## Overview

## Docker compose

Start the broker and applications:

```bash
docker compose down -v && docker compose up
```

Wait for everything to startup - approx 1 minute.

## Python producer

Open another terminal and start the PRODUCER. The CONSUMER is already listening to topic python_events:

```bash
cd python-producer
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip && pip install \
  confluent-kafka \
  pydantic
python main.py
```

## KSQLDB

Tables and stream have already been setup from `ksqldb-cli` init script. Shell into ksqldb and inspect the stream and average table:

```bash
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

Inspect the table and stream data:

```sql
select * from fruit_average_count;
select * from fruit_stream;
```

TODO: configure jdbc driver for ksqldb and DBeaver: https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc
navigating UI and download button: https://d2p6pa21dvn84.cloudfront.net/api/plugins/confluentinc/kafka-connect-jdbc/versions/10.8.0/confluentinc-kafka-connect-jdbc-10.8.0.zip

