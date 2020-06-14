Website status checker with Kafka and Postgres
==============================================
The system implemented in this repository monitors website availability over the network. It involves: 
- a `watcher` that periodically checks the target website and sends the results to Kafka
- a `recorder` that reads from Kafka and stores the data in a Postgresql database.

Database schema (Postgres)
-------------------------
    - Consists of a single table for recording checking events
    - The fields consist of `code` (HTTP status code), `response_time`, `url`, `timestamp`, `content_ok` (whether the optional regex check succeeds)
    - The create statement is in `schema.sql`

Config file:
------------
    - Contains settings such as URL to be checked as well as credentials of Kafka and Postgres 
    - Copy `config.py.example` to `config.py`
    - Change values appropriately
    
How to run:
-----------
    1) In a virtualenv, install dependencies with `make init`
    2) Run unit tests with `make test`
    3) Run the website status recorder with `make run-recorder`
    4) Run the website status watcher with `make run-watcher` (check every 10s interval) or `make run-watcher-once` (run once)
#### The website status watcher `watcher.py` accepts optional arguments such as: 
    - `--url` if specified overwrite the `SITE_TO_CHECK` in config
    - `--interval` if specified check is repeated with given interval in seconds
    - `--regex` if specified the site return text is checked against regex
