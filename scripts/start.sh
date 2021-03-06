#!/bin/bash

export NETWORK_NAME=network


# Check for NETWORK_NAME network and create it
if [ -z $(docker network ls --filter name=^${NETWORK_NAME}$ --format="{{ .Name }}") ] ; then 
    echo "Creating network '$NETWORK_NAME'"
    docker network create ${NETWORK_NAME} ; 
fi

# If called with 'build', build the project first
if [[ "$1" == build ]]
then
    docker-compose -f docker/docker-compose.yml build
fi

# start the stack
docker-compose -f docker/docker-compose.yml up -d
