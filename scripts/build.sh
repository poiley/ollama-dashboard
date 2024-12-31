#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Cleaning up old Docker resources...${NC}"

# Stop any running containers
docker-compose -f docker/docker-compose.yml down

# Remove old images
OLD_IMAGES=$(docker images "ollama-dashboard*" -q)
if [ ! -z "$OLD_IMAGES" ]; then
    echo -e "${YELLOW}Removing old images...${NC}"
    docker rmi $OLD_IMAGES
fi

# Build new image
echo -e "${YELLOW}Building new image...${NC}"
docker-compose -f docker/docker-compose.yml build --no-cache

# Start the container
echo -e "${YELLOW}Starting container...${NC}"
docker-compose -f docker/docker-compose.yml up -d

# Check if container is running
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Container is running!${NC}"
    echo -e "${GREEN}Dashboard available at: http://127.0.0.1:5000${NC}"
    echo -e "${YELLOW}Note: Make sure Ollama is running on your host machine${NC}"
else
    echo -e "${RED}Error starting container. Check logs with: docker-compose -f docker/docker-compose.yml logs${NC}"
fi 