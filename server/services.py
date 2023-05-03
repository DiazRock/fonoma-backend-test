from aioredis import Redis
import json

class OrderProcessorCache:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def process(self, json_input) -> str:
        orders, criterion = json_input.orders, json_input.criterion
        value = await self._redis.get(
                str(orders) + criterion
            )
        if not value: 
            filteredOrders = [o.json() for o in orders if o.status == criterion]
            await self._redis.set(
                str(orders) + criterion,
                json.dumps(filteredOrders)
            )
            return filteredOrders
        return json.loads(value)
