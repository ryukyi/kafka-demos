import sys
import os
import logging

import psycopg2
from confluent_kafka import Consumer, KafkaException, KafkaError
from pydantic import BaseModel, ValidationError

# Configure logging to output to STDOUT
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get DB environment vars 
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]

# Define a Pydantic model for the message
class MessageModel(BaseModel):
    number: int
    fruit: str

def connect_to_db():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
    )

def consume_messages(consumer, cursor, conn):
    """Consume messages from Kafka and process them."""
    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"Reached end of partition: {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                process_message(msg, cursor, conn)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def process_message(msg, cursor, conn):
    """Process a single Kafka message."""
    raw_message = msg.value().decode('utf-8')
    logger.info(f"Raw message: {raw_message}")

    if not raw_message.strip():
        logger.warning("Received empty message")
        return

    try:
        # Validate and parse the JSON message using Pydantic
        message_data = MessageModel.parse_raw(raw_message)
        logger.info(f"Message Data: {message_data}")

        # Insert data into the database
        cursor.execute(
            "INSERT INTO random_numbers (number, fruit) VALUES (%s, %s)",
            (message_data.number, message_data.fruit)
        )
        conn.commit()
        logger.info(f"Inserted message into DB: {message_data}")

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
    except Exception as e:
        logger.error(f"Failed to insert message into DB: {e}")

def main():
    conf = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'broker:29092'),
        'group.id': 'python-consumer-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe(['python-events'])

    conn = connect_to_db()
    cursor = conn.cursor()

    consume_messages(consumer, cursor, conn)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
