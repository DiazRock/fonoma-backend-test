# fonoma-backend-test
Backend exercise for aplying to fonoma jobs


In this exercise we need to define an endpoint for a POST request, in which we receive a payload with a list of orders and a criterion. The answer must be a list of orders, matching the criterion with the order status.

## Install dependencies on host machine

`pip install pipenv`
`pipenv install -r requirements.txt`

If you want to load the virtualenv defined by pipenv installation just do:
`pipenv shell`

On your shell of preference, mine is guake :)

## Deploying the system for production

This space is using render.com

## Deploying the for develop

There is a [local-develop.yml](./local-develop.yml) in which we have a manifest for docker-compose deploying in develop mode.

`docker-compose up --build` will build and deploy the system.

## Running test

After deploying the system we can run tests doing the following command on the host machine

`py.test --asyncio-mode=strict ./server/tests.py`