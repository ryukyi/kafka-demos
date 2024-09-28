## Overview

## Docker compose

Start the broker and applications:

```bash
docker compose down -v && docker compose up
```

## Python producer

The consumer is already listening from docker compose. We are going to run the producer. First open the UI:

```bash
http://localhost:8080
```

Now run the producer and send messages to the kafka broker:

```bash
cd python-producer
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip && pip install \
  confluent-kafka \
  pydantic \
  psycopg2-binary
python main.py
```
