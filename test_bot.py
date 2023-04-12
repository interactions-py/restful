from os import environ

import interactions
from dotenv import load_dotenv
from interactions_restful import APIExtension

load_dotenv()

client = interactions.Client()
APIExtension(client, "127.0.0.1", 56789, "flask", import_name="my-app")
# client.load_extension("interactions.ext.restful", mode="flask", host="127.0.0.1", port=54322)
client.load_extension("test_ext")


client.start(environ["TOKEN"])