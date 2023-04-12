import interactions
from interactions_restful import setup
from interactions_restful.backends.fast_api import FastAPI


client = interactions.Client()
setup(client, FastAPI, "localhost", 8000)
client.load_extension("exts.my_ext")


@interactions.listen()
async def on_startup():
    print(f"Bot `{client.user.username}` started up")


client.start("TOKEN")
