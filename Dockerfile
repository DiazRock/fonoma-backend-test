FROM python:3.10-slim-bullseye

WORKDIR /code
RUN pip install pipenv
RUN pipenv install fastapi uvicorn aioredis dependency-injector pytest pytest-asyncio pytest-cov httpx
RUN pipenv requirements
ENTRYPOINT ["pipenv", "run", "uvicorn", "server.fastapi_server:app", "--host", "0.0.0.0" ]