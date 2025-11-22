✈️ Airport API Service (Django REST Framework + Docker)

This project implements a RESTful API for managing airports, flights, 
and orders (tickets), using Python/Django, Django REST Framework, 
and a PostgreSQL database orchestrated with Docker Compose.

TECHNOLOGIES:

  --- Backend:
        Python 3.11, 
        Django 4.x

  --- API:
        Django REST Framework
  
  --- Database:
        PostgreSQL

  --- Deployment/Containerization:
        Docker,
        Docker Compose

PREREQUISITES:

To run the project locally, you must have the following installed:
  --- Docker
  --- Docker Compose

LOCAL PROJECT STARTUP:

To start the services, execute the following sequence of commands in the 
project's root directory (where the `docker-compose.yml` file is located):

1. Build Images and Run Services

This command builds the Docker images (ensuring your latest code changes are included) 
and starts all services in the background (`-d` for detached mode):

  --- docker compose build

  --- docker compose up -d

2. Database Initialization

After the first startup, you must run database migrations and create an administrator user. 
Use the docker compose run command to execute these one-time actions within your web container:

# Apply database migrations

  --- docker compose run --rm web python manage.py migrate

# Create a superuser (administrator account)

  --- docker compose run --rm web python manage.py createsuperuser

    Username: airport_admin

    Password: airport_user1234567890

# Follow the terminal prompts to set up the username and password


SERVICE ACCESS:

After a successful launch, you can access the project services at the following URLs:

  --- API Documentation (Swagger UI):  http://127.0.0.1:8000/api/docs/

  --- Django Admin Panel:  http://127.0.0.1:8000/admin/


API TESTING:

Please use the Swagger UI (/api/docs/) for testing all API endpoints.


AUTHORIZATION:

To perform POST, PUT, DELETE requests, and to view your own orders, 
you must be authorized using a JWT Token.

  1. Obtain a token (e.g., via a POST request to your designated authentication endpoint).

  2. Click the "Authorize" button in the Swagger UI and input the token in the format Bearer <your_token>.


EXAMPLE TEST (Creating an Order):

POST request to /api/airport/orders/

  --- Request Body: 
    {
      "flight_id": 1 
      // Replace 1 with the actual ID of an existing flight
    }

  --- Expected Response: 201 Created


STOPPING AND CLEANUP:

To stop and remove all running containers and networks for this project:

# Stop and remove containers and networks

  --- docker compose down

If you wish to remove the associated database volumes (and delete the data permanently), 
use the -v flag:

# Stop and remove everything, including database data

  --- docker compose down -v
