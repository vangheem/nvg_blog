from aiohttp import web
import asyncio

async def hello(request):
    await asyncio.sleep(0.5)
    return web.Response(text='done')

app = web.Application()
app.add_routes([web.get('/', hello)])

if __name__ == '__main__':
    web.run_app(app, port=8081)