#!/bin/bash
set -e

# Determine which service to run
SERVICE=${1:-disease_service}

if [ "$SERVICE" = "disease_service" ]; then
  echo "Starting Disease Detection Service..."
  # Wait for database to be ready
  echo "Waiting for PostgreSQL to be ready..."
  while ! pg_isready -h db -U disease_user -d disease_detection 2>/dev/null; do
    sleep 1
  done
  echo "Database is ready!"
  sleep 2
  # Run the FastAPI app
  exec uvicorn app.disease_service:app --host 0.0.0.0 --port 8000 --reload
  
elif [ "$SERVICE" = "notification_service" ]; then
  echo "Starting Notification Service..."
  # Wait for Kafka to be ready
  echo "Waiting for Kafka to be ready..."
  max_attempts=30
  attempt=0
  while [ $attempt -lt $max_attempts ]; do
    if python -c "import socket; socket.create_connection(('kafka', 9092), timeout=1)" 2>/dev/null; then
      echo "Kafka is ready!"
      break
    fi
    attempt=$((attempt + 1))
    sleep 1
  done
  if [ $attempt -eq $max_attempts ]; then
    echo "Kafka did not become ready in time"
    exit 1
  fi
  sleep 2
  # Run the notification service
  exec python -m app.notification_service
else
  echo "Unknown service: $SERVICE"
  exit 1
fi
