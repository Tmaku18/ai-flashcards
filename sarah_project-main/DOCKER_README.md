# Docker Setup for Flashcard App

This is a simple Docker Compose setup to run both the backend and frontend of the Flashcard App.

## Requirements

- Docker
- Docker Compose

## Running the Application

1. Make sure you are in the project root directory
2. Run the following command to start both the backend and frontend:

```bash
docker-compose up
```

3. To run in detached mode (in the background):

```bash
docker-compose up -d
```

4. To stop the application:

```bash
docker-compose down
```

## Accessing the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- API Documentation: http://localhost:8080/api/docs
- Database Explorer: http://localhost:8081

## Volumes

The Docker Compose setup includes volumes to ensure:

- Code changes in the app directory are reflected immediately
- Uploaded files are persisted
- The database is persisted

## Troubleshooting

If you encounter any issues:

1. Check the logs:

```bash
docker-compose logs
```

2. To see logs for a specific service:

```bash
docker-compose logs backend
# or
docker-compose logs frontend
```

3. To rebuild the containers after making changes to the Dockerfiles:

```bash
docker-compose build
docker-compose up
```
