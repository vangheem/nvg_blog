from aiohttp import web
import aiohttp


async def hello(request):
    try:
        session = app.session
    except AttributeError:
        session = app.session = aiohttp.ClientSession()
    async with session.get(
            'http://localhost:8081') as resp:
        return web.Response(text=await resp.text())


app = web.Application()
app.add_routes([web.get('/', hello)])


if __name__ == '__main__':
    web.run_app(app)
