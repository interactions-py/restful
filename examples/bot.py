from os import getenv

from dotenv import load_dotenv
from fastapi import WebSocket, WebSocketDisconnect

import interactions
from interactions.ext.fastapi import setup

load_dotenv()

bot = interactions.Client(getenv("TOKEN"), intents=interactions.Intents.ALL)
api = setup(bot)


@bot.event()
async def on_start():
    print("bot started")


@bot.command()
async def test_command(ctx):
    await ctx.send("Ok")


@api.route("get", "/")
async def index():
    return {"test": "yay"}


@api.get("/guilds/{guild_id}/members/{member_id}")
async def test(guild_id: int, member_id: int):
    for guild in bot.guilds:
        if int(guild.id) == guild_id:
            break
    member = await guild.get_member(member_id)
    return member._json


@api.websocket("/ws/")
async def websocket_control(websocket: WebSocket):
    """
    Before using you have to install additional requirement:
    `pip install uvicorn[standard]`
    """
    await websocket.accept()
    await websocket.send_json({"test": "yayayyayayyaya"})
    try:
        while True:
            packet = await websocket.receive_json()
            print(packet)
            # some stuff with websocket
    except WebSocketDisconnect:
        pass


bot.start()
