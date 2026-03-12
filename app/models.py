from sqlalchemy import Column, String, Boolean
from app.database import Base
import uuid


class DiseasePrediction(Base):
    """Database model for disease predictions"""
    __tablename__ = "disease_prediction"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    image_path = Column(String(255), nullable=False)
    prediction_detail = Column(String(255), nullable=False)
    healthy = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<DiseasePrediction(id={self.id}, healthy={self.healthy})>"
