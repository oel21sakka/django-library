# Django Library Management System

This project is a Django-based Library Management System with RESTful API endpoints and real-time notifications using WebSockets.

## Prerequisites

- Docker
- Docker Compose
- Postman (for API testing)

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/oel21sakka/django-library.git
   cd django-library
   ```

2. The project includes a `.env` file with default settings. You can modify these as needed:
   ```
   SECRET_KEY='django-secret'
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1,web
   DB_NAME=django-library
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   REDIS_URL=redis://redis:6379/0
   RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//
   ```

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. The application should now be running at `http://localhost:8000`.

## Project Structure

The project uses the following services:
- Django web application
- PostgreSQL database
- Redis for caching and Channels
- RabbitMQ for Celery task queue
- Celery worker and beat for background tasks

## API Documentation

Import the provided Postman collection (`Django Library API.postman_collection.json`) into Postman to explore and test the API endpoints.

### Available Resources
- Authors
- Categories
- Books
- Libraries
- Book Availabilities
- Loans
- Users (Registration and Authentication)

### Using the Postman Collection
1. Open Postman and import the JSON file.
2. Set up an environment variable `base_url` with the value `http://localhost:8000`.
3. Use the requests in the collection to interact with the API.

## Testing WebSockets with Postman

1. In Postman, create a new WebSocket request.
2. Set the WebSocket URL to `ws://localhost:8000/ws/notifications/`.
3. Click "Connect" to establish the WebSocket connection.
4. To simulate a book becoming available, use the "Return Book" API endpoint in the Postman collection.
5. You should receive a real-time message in the WebSocket connection when a book becomes available.

## Running Celery Tasks

Celery tasks are used for sending emails and reminders. They are automatically started with Docker Compose. To manually trigger the send reminders task:

```
docker-compose exec web python manage.py send_reminders
```


## Development

To make changes to the project:

1. Modify the code as needed.
2. Rebuild and restart the Docker containers:
   ```
   docker-compose down
   docker-compose up --build
   ```