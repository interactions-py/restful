from interactions import Extension, slash_command
from interactions_restful import route


class MyExtension(Extension):
    @route("GET", "/")
    async def index(self):
        return {"data": "hello interactions.py"}

    @slash_command()
    async def command(self, ctx):
        await ctx.send("hello, api!")
