## Overview

## Docker compose

Start the broker and applications:

```bash
docker compose down -v && docker compose up
```

## KSQLDB

Open a new terminal to view live stream transforms:

```bash
http://localhost:8088
```

## Python producer

The CONSUMER is listening but the PRODUCER is not. Run the producer:

```bash
cd python-producer
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip && pip install \
  confluent-kafka \
  pydantic
python main.py
```
