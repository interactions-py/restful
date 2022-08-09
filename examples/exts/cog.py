from interactions import Extension, extension_command
from interactions.ext.fastapi import route


class Cog(Extension):
    @extension_command(
        name="ext_cmd",
        description="some desc",
    )
    async def some_command(self, ctx):
        await ctx.send("cool")

    @route("GET", "/test/")
    async def test_fast_api(self):
        return {"test": "cooooool"}


def setup(bot):
    Cog(bot)
