# Container Monitor

This is a simple docker container monitor. It starts a container which uses the its hosts instance of docker to check the health status of a list of containers running on the host. If any containers are unhealthy it sends an email alert.

## Requirements

- Docker
- Gmail account to send alerts from

## Configure

The configuration file is config.txt, replace all the capitalized strings following the colons with strings of your choice. More details on the configuration options below:

- from_email:ALERT_GMAIL_ACCOUNT &rarr; Email address to send the alerts from.

- from_email_pwd:ALERT_GMAIL_PASSWORD &rarr; Password for the email address to send the alerts from.

- email_subject:ALERT_SUBJECT &rarr; Subject of the alert email.

- recipient:ALERT_RECIPIENT_EMAIL &rarr; Recipient of the alert email.

- smtp_server:smtp.gmail.com &rarr; Gmail smtp server.

- wait_time:300 &rarr; Time in seconds to wait between container health checks.

- containers:NAME_OF_CONTAINER_1,NAME_OF_CONTAINER_2 &rarr; List of containers to check the health of.

## Run

- `docker network create -d bridge container_network`
- `docker compose up`

## Run Tests

- `python3 -m pytest`

# Notes

- This repo was ported from a private repo for [www.swampyankeetech.com](www.swampyankeetech.com), as such it has not been fully tested as the incentives to update and maintain this repo a nil.

- Not sure the docker network is necessary, it was ported from the private repo.