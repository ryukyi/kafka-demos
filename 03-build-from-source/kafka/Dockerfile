# Use an official Ubuntu image as a parent image
FROM ubuntu:latest

# Install necessary packages including ca-certificates, and clean up
RUN apt-get update && \
    apt-get install -y \
    curl \
    tar \
    ca-certificates \
    vim \
    openjdk-11-jdk \
    --no-install-recommends && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /opt

# Download Kafka source tarball and setup
RUN curl -O https://dlcdn.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz && \
    tar -xzf kafka_2.13-3.8.0.tgz && \
    rm kafka_2.13-3.8.0.tgz && \
    cd kafka_2.13-3.8.0 && \
    chmod +x ./bin/*.sh

