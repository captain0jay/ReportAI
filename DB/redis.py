import redis
import json
import os
from dotenv import load_dotenv
load_dotenv()

class RedisQueue:
    def __init__(self, name, namespace='queue'):
        host = os.environ.get('REDIS_HOST', 'localhost')
        port = int(os.environ.get('REDIS_PORT', 6379))
        db = int(os.environ.get('REDIS_DB', 0))

        self.db = redis.Redis(host=host, port=port, db=db)
        self.key = f'{namespace}:{name}'

    def enqueue(self, item):
        """Add item to the queue"""
        self.db.lpush(self.key, json.dumps(item))

    def dequeue(self, timeout=0):
        """Get item from the queue. Blocks if timeout > 0"""
        item = self.db.brpop(self.key, timeout=timeout)
        if item:
            return json.loads(item[1])
        return None
