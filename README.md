# App Aggregator

App Aggregator is a Django Rest Framework project that aggregates various apps' data from Playstore url. It uses Django Rest Framework, PostgreSQL, Docker for containerization, JWT token for authorization, and DRF Spectacular for Swagger documentation.

## Steps to Run Locally

1. Clone the repository:

    ```bash
    git clone https://github.com/NeerajN10/AppAggregator.git
    ```

2. Change to the project directory:

    ```bash
    cd AppAggregator
    ```

3. Copy the `.env.sample` file to `.env` and update the environment variables accordingly:

    ```bash
    cp .env.sample .env
    ```

    Update the `.env` file with appropriate values for your local environment.

4. Build Docker containers:

    ```bash
    docker-compose build
    ```

5. Run Docker containers:

    ```bash
    docker-compose up
    ```

6. Access the application in your browser:

    [http://localhost:8000/](http://localhost:8000/)

7. Default superuser credentials:

    - Username: admin
    - Password: admin

## API Documentation

Swagger documentation is available for the APIs. After running the project, you can access it at:

[http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
