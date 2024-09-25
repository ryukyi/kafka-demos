from confluent_kafka import Consumer, KafkaException
import sys

# Define the Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Ensure this matches your broker's advertised listener
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Create a Consumer instance
consumer = Consumer(**conf)

# Subscribe to the topic
consumer.subscribe(['python-events'])

try:
    while True:
        # Poll for new messages
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                # End of partition event
                sys.stderr.write(f"%% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n")
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            # Print the message key and value
            print(f"Received message: {msg.key().decode('utf-8')} - {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass
finally:
    # Close the consumer to commit final offsets
    consumer.close()

