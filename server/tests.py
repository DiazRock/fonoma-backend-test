"""Tests module."""

from unittest import mock

import pytest
from httpx import AsyncClient

from .fastapi_server import app, container
from .services import OrderProcessorCache


@pytest.fixture
def client(event_loop):
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    event_loop.run_until_complete(client.aclose())


@pytest.mark.asyncio
async def test_process_orders(client):
    return_value = {"result":
                    ["{\"id\": 1, \"item\": \"Laptop\", \"quantity\": 1, \"price\": 999.99, \"status\": \"completed\"}",
                    "{\"id\": 3, \"item\": \"Headphones\", \"quantity\": 3, \"price\": 99.9, \"status\": \"completed\"}"]}
    input_value = '{"orders": [{"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},{"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},{"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},{"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}],"criterion": "completed"}'
    service_mock = mock.AsyncMock(spec=OrderProcessorCache)
    service_mock.process.return_value = return_value

    with container.service.override(service_mock):
        response = await client.post("/solution", content= input_value)

    assert response.status_code == 200
    assert response.json() == return_value

@pytest.mark.asyncio
async def test_process_orders_bad_request(client):
    return_value = {"detail": "No orders provided"}
    input_value = '{"orders": [],"criterion": "completed"}'
    service_mock = mock.AsyncMock(spec=OrderProcessorCache)
    service_mock.process.return_value = return_value

    with container.service.override(service_mock):
        response = await client.post("/solution", content= input_value)

    assert response.status_code == 400
    assert response.json() == return_value


@pytest.mark.asyncio
async def test_process_orders_bad_price(client):
    return_value = {"detail": "Order price must be positive"}
    input_value = '{"orders": ["{\"id\": 1, \"item\": \"Laptop\", \"quantity\": 1, \"price\": -999.99, \"status\": \"completed\"}"],"criterion": "completed"}'
    service_mock = mock.AsyncMock(spec=OrderProcessorCache)
    service_mock.process.return_value = return_value

    with container.service.override(service_mock):
        response = await client.post("/solution", content= input_value)
    assert response.status_code == 422
    #assert response.json() == return_value