-- Create the initial stream from the Kafka topic
CREATE STREAM fruit_stream (
    number INT,
    fruit STRING
) WITH (
    KAFKA_TOPIC='fruit-topic',
    VALUE_FORMAT='JSON'
);

-- Create a table to calculate the average number over a 1-minute tumbling window
CREATE TABLE fruit_average_count WITH (KAFKA_TOPIC='fruit-average-count-topic') AS
SELECT
  fruit,
  AVG(number) AS average_count
FROM
  fruit_stream
WINDOW TUMBLING (SIZE 1 MINUTE)
GROUP BY
  fruit
EMIT CHANGES;

