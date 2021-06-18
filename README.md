# pyredq
Light and fast ordered message queue for Python3, leveraging Redis lists. Uses [MessagePack](https://msgpack.org/) for efficient message serialization.

## Install
```
pip3 install pyredq
```

## Usage
### Publisher
```python
import pyredq

queue = pyredq.RedisQueue()

queue.put("queue1", "a message")
```

### Consumer
```python
import pyredq

queue = pyredq.RedisQueue()

def handler(message):
    print(message)
    # "a message"

queue.subscribe("queue1", handler)
```

Subscribe also works in the background (non-blocking):
```python
queue.subscribe("queue1", handler, background=True)

# Do other stuff
```

### Redis configuration
`pyredq.RedisQueue()` takes standard [Redis client parameters](https://redis-py.readthedocs.io/en/stable/#redis.Redis) as arguments, such as:
```python
queue = pyredq.RedisQueue(host="redis", port=6379, db=0, socket_timeout=0.2, retry_on_timeout=True)
```
