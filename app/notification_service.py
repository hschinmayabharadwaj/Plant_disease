import json
import logging
from kafka import KafkaConsumer
from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NotificationService:
    """Consumes events from disease.events Kafka topic and sends notifications"""

    def __init__(self):
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='notification-group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def start_consuming(self):
        """Start consuming messages from Kafka topic"""
        logger.info(f"Notification Service started. Listening to topic: {KAFKA_TOPIC}")
        
        try:
            for message in self.consumer:
                self.process_message(message.value)
        except KeyboardInterrupt:
            logger.info("Shutting down Notification Service")
        finally:
            self.consumer.close()

    def process_message(self, event_data: dict):
        """Process and print prediction details"""
        try:
            pred_id = event_data.get('pred_id')
            healthy = event_data.get('healthy')
            
            # Print prediction details
            logger.info("=" * 60)
            logger.info("🔔 DISEASE PREDICTION NOTIFICATION 🔔")
            logger.info(f"Prediction ID: {pred_id}")
            logger.info(f"Status: {'Healthy' if healthy == 'yes' else 'Disease Detected'}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")


def main():
    """Main entry point for notification service"""
    service = NotificationService()
    service.start_consuming()


if __name__ == "__main__":
    main()
