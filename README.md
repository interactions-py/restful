# interactions restful

A library for interactions.py allowing runtime API structures

## Installation

Using pip:
`pip install interactions-restful`

Using poetry:
`poetry add interactions-restful`

Don't forget to specify backend you want to use:
- [FastAPI](https://fastapi.tiangolo.com/): `pip install interactions-restful[fastapi]`
- [Quart](https://pgjones.gitlab.io/quart/index.html): `pip install interactions-restful[quart]`

Also make sure to install an ASGI server:
- [Uvicorn](https://www.uvicorn.org/): `pip install interactions-restful[uvicorn]`
- [Hypercorn](https://pgjones.gitlab.io/hypercorn/): `pip install interactions-restful[hypercorn]`
- [Daphne](https://github.com/django/daphne): `pip install interactions-restful[daphne]`

You can also install both your backend and ASGI server at once, for example
`pip install interactions-restful[fastapi,uvicorn]`

## Simple (FastAPI) example

### Main file
- `main.py`

```python
import interactions
from fastapi import FastAPI
from interactions_restful.backends.fastapi import FastAPIHandler

app = FastAPI()

client = interactions.Client(token="token")
FastAPIHandler(client, app)

client.load_extension("api")
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

### Run

```bash
uvicorn main:app --reload
```

## Backends

Currently, the library support only Quart and FastAPI as a backend for building an API, but if you don't want to use them you can create own backend.
