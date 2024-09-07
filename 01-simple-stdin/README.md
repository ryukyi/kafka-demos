To simulate data streaming.

### Quickstart

```bash
./setup-
docker compose down # make sure no other compose instances are running
docker compose up -d
```

#### Step 1: Create a Kafka Topic

First, create a Kafka topic where you will send and receive messages. 
You can do this using the Kafka topics command line tool:

```bash
docker exec -it kafka \
  kafka-topics --create \
  --topic test-topic \
  --partitions 1 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092
```

This command creates a topic named `test-topic` with one partition and a replication factor of one.

#### Step 2: Start the Kafka Console Producer

The Kafka console producer reads lines from standard input and sends them to a Kafka topic. Start the producer by running:

```bash
docker exec -it kafka \
  kafka-console-producer \
  --topic test-topic \
  --bootstrap-server localhost:9092
```

Once the producer is running, you can type messages into the terminal.
Each line you enter will be sent as a separate message to the Kafka topic `test-topic`.

#### Step 3: Start the Kafka Console Consumer

In a new terminal window, start the Kafka console consumer to read messages from the topic. Run:

```bash
docker exec -it kafka \
  kafka-console-consumer \
  --topic test-topic \
  --from-beginning \
  --bootstrap-server localhost:9092
```

The consumer will read messages from the topic and print them to the terminal.
The `--from-beginning` flag tells the consumer to read all messages in the topic from the start.

#### Step 4: Simulate Data Streaming

With both the producer and consumer running, you can simulate data streaming:

- In the producer terminal, type messages and hit enter. Each message represents a data event being sent to Kafka.
- Switch to the consumer terminal to see the messages being received and displayed.

This setup allows you to manually simulate producing and consuming data streams using Kafka.

### Summary

By using Kafka's console producer and consumer tools, you can easily simulate data streaming in your local Kafka environment set up with Docker Compose. This method is excellent for development and testing to understand how Kafka handles data streaming without needing to integrate with actual producer and consumer applications initially.

