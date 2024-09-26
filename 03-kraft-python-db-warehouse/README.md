## Overview

## Docker compose

Start the broker and applications then remove the initializing script

```bash
docker compose up -d && \
docker compose stop init-broker && \
docker compose rm init-broker
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
