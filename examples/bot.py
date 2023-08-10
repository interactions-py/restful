import interactions
from fastapi import FastAPI

from interactions_restful.backends.fastapi import FastAPIHandler

app = FastAPI()
client = interactions.Client(token="TOKEN")
FastAPIHandler(client, app)

client.load_extension("exts.my_ext")


@interactions.listen()
async def on_startup():
    print(f"Bot `{client.user.username}` started up")
