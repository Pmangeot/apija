# Fastapi Project Template

A FastAPI personal template using Docker that includes **SMTPServer**, **Postgres**.
The API is configured to allow SQL request only through datamapper

## Installation

```sh
$ git clone https://github.com/Pmangeot/apija.git
$ cd apija
$ code .
```

Once in your IDE, you need to configure the /core/config.py file with the env variables needed.
You should also modify the endpoints, that are mere examples of code, and add you sql initialisation script directly in the /db/migration.sql file

Once modified you can launch the container with docker : ```docker compose up --build```

## Use

Swagger documentation is reachable in the /docs route of the base URL
Pytest can be launched directly from the docker termainl with the commande ```pytest```

## Evolutions

This code is my personal starting point for a new api and will be corrected in the future.
Additional functionalities to be implemented are mainly an FTP server and Pytest.