#! /bin/bash
# something wrong with permissions how the data dir is generated from docker compose

mkdir -p ./data/kafka
# Change the owner of the directory to user ID 1000 and group ID 1000
sudo chown 1000:1000 ./data/kafka
# Set the directory permissions to ensure read, write, and execute permissions for the owner
sudo chmod 700 ./data/kafka

