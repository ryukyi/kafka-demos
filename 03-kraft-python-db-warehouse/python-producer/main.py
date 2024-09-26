import os
import logging

from confluent_kafka import Producer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:29092")
# Kafka producer configuration
conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'log_level': 7,
    'debug': 'all',
    'logger': logger
}

# Create Producer instance
producer = Producer(conf)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Produce messages
for i in range(10):
    producer.produce('python-events', key=str(i), value=f'message {i}', callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report callbacks to be triggered.
producer.flush()

