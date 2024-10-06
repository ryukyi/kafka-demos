from confluent_kafka import Producer
import json
import socket
import random

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
        producer.produce('python-events', key=str(i), value=json.dumps(message), callback=delivery_report)
        producer.poll(0)  # Trigger delivery report callbacks

    producer.flush()  # Wait for all messages to be delivered

if __name__ == "__main__":
    produce_messages()
