# Disease Detection System

A FastAPI-based disease detection system with Kafka event streaming and PostgreSQL database.

## Architecture

The system consists of:

1. **Disease Detection Service** - FastAPI REST API
   - POST `/predict` - Accepts image files for disease detection
   - GET `/health` - Health check endpoint
   - Stores predictions in PostgreSQL
   - Publishes events to Kafka

2. **Notification Service** - Kafka Consumer
   - Consumes events from `disease.events` topic
   - Logs prediction notifications

3. **Database** - PostgreSQL
   - Stores disease predictions with UUID, image path, prediction detail, and health status

4. **Message Broker** - Kafka
   - Topic: `disease.events`
   - Handles event streaming between services

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### Running with Docker Compose

```bash
docker-compose up --build
```

This starts:
- PostgreSQL on port 5432
- Kafka on port 29092
- Disease Detection Service on port 8000
- Notification Service (processing Kafka events)

### Using the API

**Upload an image for disease detection:**

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@image.jpg"
```

**Response:**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "image_path": "images/123e4567-e89b-12d3-a456-426614174000.jpg",
  "prediction_detail": "Healthy",
  "healthy": true
}
```

**Health check:**

```bash
curl http://localhost:8000/health
```

## Project Structure

```
disease_detection_system/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuration settings
│   ├── database.py               # Database setup and session
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── schemas.py                # Pydantic schemas
│   ├── disease_service.py        # Disease Detection Service (FastAPI)
│   ├── kafka_producer.py         # Kafka event producer
│   └── notification_service.py   # Notification Service (Kafka consumer)
├── images/                       # Stored prediction images
├── Dockerfile                    # Container image definition
├── docker-compose.yml            # Multi-container setup
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Database Schema

**Table: disease_prediction**

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR(36) | UUID primary key |
| image_path | VARCHAR(255) | Path to stored image |
| prediction_detail | VARCHAR(255) | Prediction result text |
| healthy | BOOLEAN | True if healthy, False if disease detected |

## Kafka Events

**Topic: disease.events**

Event payload:

```json
{
  "pred_id": "123e4567-e89b-12d3-a456-426614174000",
  "healthy": "yes"
}
```

## Environment Variables

Create a `.env` file to override defaults:

```env
DATABASE_URL=postgresql://disease_user:disease_password@db:5432/disease_detection
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

## Local Development

Without Docker:

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Set up PostgreSQL** and **Kafka** locally (or use Docker for these)

3. **Run Disease Detection Service:**

```bash
uvicorn app.disease_service:app --reload
```

4. **Run Notification Service** (in another terminal):

```bash
python -m app.notification_service
```

## API Documentation

Once running, visit: `http://localhost:8000/docs` (Swagger UI)

## Logs

View notification service logs:

```bash
docker-compose logs -f notification_service
```

## Stopping Services

```bash
docker-compose down
```

To remove volumes:

```bash
docker-compose down -v
```

## Future Enhancements

- Integrate actual ML model for disease detection
- Add authentication to API endpoints
- Implement image validation
- Add support for multiple disease types
- Create web UI for results
- Add metrics and monitoring
