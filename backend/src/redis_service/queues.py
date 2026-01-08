import json
from .connection import redis_client

class Queue:
    def __init__(self, queue: str):
        self.queue = queue

    async def push_task(self, task: dict):
        await redis_client.lpush(self.queue, json.dumps(task))

    async def pop_task(self):
        result = await redis_client.brpop(self.queue, timeout=0)
        if result is None:
            return None
        #gettting data without key
        data = result[1]
        return json.loads(data)
