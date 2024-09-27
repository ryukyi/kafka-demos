import sys
import logging
from confluent_kafka import Producer

# Configure logging to output to STDOUT
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_messages():
    conf = {
        'bootstrap.servers':'localhost:9092'
    }

    producer = Producer(conf)

    try:
        for i in range(10):  # Example: produce 10 messages
            message = f"Message {i}"
            producer.produce('python-events', message.encode('utf-8'), callback=delivery_report)
            producer.poll(0)  # Serve delivery reports (callbacks)

        producer.flush()  # Wait for all messages to be delivered

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Exiting gracefully...")
        producer.flush()  # Ensure all messages are delivered before exiting
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    try:
        produce_messages()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting...")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
