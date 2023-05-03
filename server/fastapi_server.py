"""Fast api server module."""

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import json

from .containers import Container
from .services import OrderProcessorCache


app = FastAPI()

class Order(BaseModel):
    id: int
    item: str
    quantity: int    
    price: float
    status: str 

class OrderRequest(BaseModel):
    criterion: str
    orders: List[Order]

@app.post("/solution")
@inject
async def process_orders(orders_and_criterion: OrderRequest, service: OrderProcessorCache = Depends(Provide[Container.service])):
    if len(orders_and_criterion.orders) == 0:
        raise HTTPException(status_code = 400, detail="No orders provided")
    if any(o.price <= 0 for o in orders_and_criterion.orders):
        raise HTTPException(status_code = 422, detail="Order price must be positive")

    value = await service.process(orders_and_criterion)
    return value


container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost")
container.wire(modules=[__name__])
