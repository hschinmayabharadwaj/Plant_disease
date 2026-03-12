import json
from kafka import KafkaProducer
from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from app.schemas import PredictionEvent


class DiseaseEventProducer:
    """Producer for disease.events Kafka topic"""

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=3
        )
        self.topic = KAFKA_TOPIC

    def send_event(self, pred_id: str, healthy: bool):
        """Send prediction event to Kafka topic"""
        event = PredictionEvent(
            pred_id=pred_id,
            healthy="yes" if healthy else "no"
        )
        self.producer.send(self.topic, value=event.model_dump())
        self.producer.flush()

    def close(self):
        """Close producer connection"""
        self.producer.close()
