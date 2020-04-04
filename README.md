# airflow-docker

**Dockerfile** of [Airflow](https://github.com/apache/airflow)

## Info

* Python 3.7.1-slim-stretch [Official Image](https://hub.docker.com/_/python)

## Usage

Pull the image

    docker pull namcx/airflow-docker

By default, airflow-docker runs Airflow with **LocalExecutor** :

    docker run -d -p 8080:8080 namcx/airflow-docker webserver
