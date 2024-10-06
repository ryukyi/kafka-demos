import json
import socket
import random
from time import sleep

from confluent_kafka import Producer

# Callback for delivery reports
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Set up Kafka producer
# NOTE: localhost used as host since that's what is declared as EXTERNAL in Kafka config
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': socket.gethostname()
}

producer = Producer(conf)

# List of random fruits
fruits = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 'kiwi', 'lemon']

ONE_HUNDRED_THOUSAND = 100_000
# Function to send messages to Kafka
def produce_messages():
    for i in range(ONE_HUNDRED_THOUSAND):
        # Select a random fruit from the list
        fruit = random.choice(fruits)
        message = {'number': i, 'fruit': fruit}
        producer.produce('fruit-topic', key=str(i), value=json.dumps(message), callback=delivery_report)
        producer.poll(0)  # Trigger delivery report callbacks
        sleep(0.33)

    producer.flush()  # Wait for all messages to be delivered

if __name__ == "__main__":
    produce_messages()
