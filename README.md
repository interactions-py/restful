# interactions restful

A library for interactions.py allowing runtime API structures

## Installation

Using pip:  
`pip install interactions-restful`

Using poetry:  
`poetry add interactions-restful`

Don't forget to specify backend you want to use:
- flask `pip install interactions-restful[flask]`
- fastapi  `pip install interactions-restful[fastapi]`

## Simple example

### Main file

```python
import interactions
from interactions_restful import setup
from interactions_restful.backends.fast_api import FastAPI

client = interactions.Client()

setup(client, FastAPI, "127.0.0.1", 5000)

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
        return {"status": "Hello, i.py"}
    
    @interactions.slash_command()
    async def test_command(self, ctx):
        await ctx.send("Hello, API")

```

## Backends

Currently, library support only flask and fastapi as a backend for building an api, but if you don't want to use them you can create own backend.

## Documentation

[FastAPI documentation](https://fastapi.tiangolo.com/)
