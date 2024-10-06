-- Create the initial stream from the Kafka topic
CREATE STREAM python_events_stream (
    number INT,
    fruit STRING
) WITH (
    KAFKA_TOPIC='python-events',
    VALUE_FORMAT='JSON'
);

-- Create a table to calculate the average number over a 1-minute tumbling window
CREATE TABLE average_number_table WITH (KAFKA_TOPIC='average_number_topic') AS
SELECT
  fruit,
  AVG(number) AS average_number
FROM
  python_events_stream
WINDOW TUMBLING (SIZE 1 MINUTE)
GROUP BY
  fruit
EMIT CHANGES;

