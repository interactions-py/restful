# FastAPI wrapper for interactions.py

An Extension library to add API for your interactions.py bot by using Fast API.

## Installation

``pip install git+https://github.com/Damego/interactions-fastapi.git``


## Examples

```python
import interactions
from interactions.ext.api import setup

client = interactions.Client(...)
api = setup(client)

@api.route("GET", "/")
async def index():
    return {"status": "success"}

client.start()
```

Server will run on ``127.0.0.1:32512`` (host and port modifiable)

More examples in ``examples`` folder.
