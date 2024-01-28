# App Aggregator

App Aggregator is a Django Rest Framework project that aggregates various apps' data from Playstore url. It uses Django Rest Framework, PostgreSQL, Docker for containerization, JWT token for authorization, DRF Spectacular for Swagger documentation and Grafana with Prometheus for analytics.

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


## Grafana Integration

Enhance your monitoring experience with Grafana integration, providing insightful visualizations and dashboards for your application metrics. Access Grafana at:

[http://localhost:3000/](http://localhost:3000/)

We are using Prometheus to collect metrics.

Explore a variety of templates available on [Grafana Dashboards](https://grafana.com/grafana/dashboards/) to customize your monitoring setup.

Here is a sample screenshot of the Grafana dashboard with UID: [7996](https://grafana.com/grafana/dashboards/7996-django-prometheus/):

![image](https://github.com/NeerajN10/AppAggregator/assets/22143118/521115e9-7d96-44c4-b52c-3a08c171c32b)
