FROM python:3.12-slim
WORKDIR /app
COPY ./main.py ./main.py
RUN pip install --no-cache-dir confluent-kafka psycopg2-binary pydantic
CMD ["python", "main.py"]
