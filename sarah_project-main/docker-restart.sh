#!/bin/bash

echo "Stopping containers..."
docker-compose down

echo "Rebuilding containers..."
docker-compose build

echo "Starting containers..."
docker-compose up -d

echo "Containers are now running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8080"
echo "API Docs: http://localhost:8080/api/docs"
echo "DB Explorer: http://localhost:8081"
echo ""
echo "To view logs, run: docker-compose logs -f"
