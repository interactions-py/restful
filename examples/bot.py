import interactions

from interactions_restful import setup
from interactions_restful.backends.fastapi import FastAPIHandler

client = interactions.Client()
setup(client, FastAPIHandler, "localhost", 8000)
client.load_extension("exts.my_ext")


@interactions.listen()
async def on_startup():
    print(f"Bot `{client.user.username}` started up")


client.start("TOKEN")
