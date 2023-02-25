# FastAPI wrapper for interactions.py

An Extension library to add restful API for your interactions.py bot.

## Installation

``pip install interactions-restful``

## Simple example

### Main file

```python
import interactions
from interactions_restful import APIExtension

client = interactions.Client()

APIExtension(client, "127.0.0.1", 5000, "flask")

client.load_extension("api")

client.start("token")
```

### Extension file
- `api.py`

```python
import interactions
from interactions_restful import route


class MyAPI(interactions.Extension):
    @route("GET", "/")
    def index(self):
        return {"status": "success"}

```

## Modes

Extension support both flask and fastapi as backend for building an api, but if you don't want to use them you could create own backend.

## Documentation

[FastAPI documentation](https://fastapi.tiangolo.com/)
