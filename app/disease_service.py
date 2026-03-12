import os
import uuid
import random
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db, create_tables
from app.models import DiseasePrediction
from app.schemas import PredictionResponse
from app.kafka_producer import DiseaseEventProducer
from app.config import IMAGES_DIR

app = FastAPI(title="Disease Detection Service")

# Initialize Kafka producer
producer = DiseaseEventProducer()


@app.on_event("startup")
async def startup():
    """Initialize database tables on startup"""
    create_tables()


@app.on_event("shutdown")
async def shutdown():
    """Close Kafka producer on shutdown"""
    producer.close()


@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    POST API to submit image for disease detection.
    
    1. Stores image file within docker
    2. Randomly predicts yes/no
    3. Stores result in database
    4. Produces event to Kafka topic
    """
    try:
        # Generate unique ID for this prediction
        pred_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_extension = os.path.splitext(file.filename)[1]
        image_filename = f"{pred_id}{file_extension}"
        image_path = os.path.join(IMAGES_DIR, image_filename)
        
        # Save file to disk
        contents = await file.read()
        with open(image_path, "wb") as f:
            f.write(contents)
        
        # Mock ML prediction - randomly predict healthy or diseased
        is_healthy = random.choice([True, False])
        prediction_detail = "Healthy" if is_healthy else "Disease Detected"
        
        # Store result in database
        db_prediction = DiseasePrediction(
            id=pred_id,
            image_path=f"images/{image_filename}",
            prediction_detail=prediction_detail,
            healthy=is_healthy
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        # Send event to Kafka topic
        producer.send_event(pred_id, is_healthy)
        
        return PredictionResponse(
            id=db_prediction.id,
            image_path=db_prediction.image_path,
            prediction_detail=db_prediction.prediction_detail,
            healthy=db_prediction.healthy
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error processing image: {str(e)}"}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "Disease Detection Service is running"}
