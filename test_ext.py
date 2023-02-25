from interactions import Extension

from interactions_restful import route

class MyApi(Extension):
    @route("GET", "/")
    async def index(self):
        return {"data": "hello world"}
