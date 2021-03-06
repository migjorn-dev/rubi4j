#!/bin/sh
# 
# run-docker.sh
# Version 1.1 (20.4.2022)
#
# start a docker container with latest neo4j version
# you need to create a network first using
#
#  # docker network create neo4j-network
#
# neo4j will store all data under /var/rubi4j so make sure this is a directory you have write permissions on.
# password will be set to rubi4j so you cann access and use neo4j instance via
#
# http://localhost:7474
#
# the docker parameters achieve the following:
# - open ports 747 and 7687 on docker machine to the container
# - connect data, logs, import and plugins directory for persistence
# - define login credentials to be Login: neo4j and Password: rubi4j
# - activate apoc (Awesome Procedures on Cypher) plugin


echo "# start neo4j for rubi4j in a docker container"

if [ ! -d /var/rubi4j ]; then
    echo "## missing /var/rubi4j"
    exit 1
fi

mkdir -p /var/rubi4j/data
mkdir -p /var/rubi4j/logs
mkdir -p /var/rubi4j/import
mkdir -p /var/rubi4j/plugins

docker run \
    --name rubi4j-neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v /var/rubi4j/data:/data \
    -v /var/rubi4j/logs:/logs \
    -v /var/rubi4j/import:/var/lib/neo4j/import \
    -v /var/rubi4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/rubi4j \
    --env NEO4JLABS_PLUGINS='["apoc"]' \
    --network neo4j-network \
    neo4j:latest

if [ $? -eq 0 ]; then
    echo "# success"
else 
    echo "## failed"
fi
