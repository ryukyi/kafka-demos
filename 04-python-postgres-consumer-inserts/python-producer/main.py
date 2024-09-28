import sys
import logging
from random import randint, choice
import trio

from confluent_kafka import Producer
from pydantic import BaseModel, ValidationError

# Configure logging to output to STDOUT
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define a Pydantic model for the message
class MessageModel(BaseModel):
    number: int
    fruit: str

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

async def produce_message(producer, number, fruit):
    """ Asynchronously produce a single message. """
    try:
        json_message = MessageModel(number=number, fruit=fruit).model_dump_json()
        logger.debug(f"Producing message: {json_message}")
        producer.produce('python-events', json_message, callback=delivery_report)
        producer.poll(0)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
    except Exception as e:
        logger.error(f"An error occurred while producing message: {e}")

async def produce_messages():
    conf = {
        'bootstrap.servers': 'localhost:9092'
    }

    producer = Producer(conf)

    # Define a list of fruits (acting as an enum)
    fruits = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry']

    # One million messages
    one_million = 1_000_000
    async with trio.open_nursery() as nursery:
        for _ in range(one_million):
            number = randint(1, 20)
            fruit = choice(fruits)
            nursery.start_soon(produce_message, producer, number, fruit)

    # Wait for all messages to be delivered
    producer.flush()

if __name__ == '__main__':
    try:
        trio.run(produce_messages)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting...")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
