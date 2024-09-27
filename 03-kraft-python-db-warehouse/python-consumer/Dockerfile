FROM python:3.12-slim
WORKDIR /app
COPY ./main.py ./main.py
RUN pip install --no-cache-dir confluent-kafka
CMD ["python", "main.py"]
