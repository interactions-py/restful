from os import getenv

from dotenv import load_dotenv

import interactions
from interactions.ext.api import APIClient

load_dotenv()

bot = interactions.Client(getenv("TOKEN"), disable_sync=True, intents=interactions.Intents.ALL)
api = APIClient(bot)
bot.load("exts.cog")


@bot.event()
async def on_start():
    print("bot started")


@api.route("get", "/guilds/{guild_id}/members/{member_id}")
async def test(guild_id: int, member_id: int):
    for guild in bot.guilds:
        if int(guild.id) == guild_id:
            break
    member = await guild.get_member(member_id)
    return member._json


api.start()
