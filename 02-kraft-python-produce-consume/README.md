## Overview

## Docker compose

```bash
docker compose up -d
```

## Configure Kafka using Kraft scripts

Shell into the container where the scripts are:

```bash
docker exec -it -w /opt/kafka/bin broker sh
```

## Create a topic

```bash
./kafka-topics.sh --create --topic python-events --bootstrap-server broker:9092
```

## Python consumer and producer

We will read and write using python. First setup the virtual env using python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip && pip install confluent-kafka
```

## Start Consumer

Setup the python consumer to listen for events on the topic:

```bash
python -m python-consumer.main
```

## Create events from a producer

In a new terminal, run python producer to send messages:

```bash
python -m python-producer.main
```

Now check the consumer to see the messages show.
