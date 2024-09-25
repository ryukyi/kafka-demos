from confluent_kafka import Producer
import os

# Get Kafka bootstrap servers from environment
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Define the Kafka configuration
conf = {
    'bootstrap.servers': bootstrap_servers
}

# Create a Producer instance
producer = Producer(**conf)

# Define a delivery report callback function
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Produce some messages
for i in range(10):
    # Produce a message asynchronously
    producer.produce('python-events', key=str(i), value=f'This is message {i}', callback=delivery_report)

    # Wait up to 1 second for events. Callbacks will be invoked during
    # this method call if the message is acknowledged.
    producer.poll(1)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
producer.flush()
