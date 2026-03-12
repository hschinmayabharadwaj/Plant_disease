from pydantic import BaseModel
from typing import Optional


class PredictionResponse(BaseModel):
    """Response schema for prediction"""
    id: str
    image_path: str
    prediction_detail: str
    healthy: bool

    class Config:
        from_attributes = True


class PredictionEvent(BaseModel):
    """Kafka event schema for disease prediction"""
    pred_id: str
    healthy: str  # "yes" or "no"
