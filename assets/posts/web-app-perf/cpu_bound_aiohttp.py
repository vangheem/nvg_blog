from aiohttp import web
import time


DURATION = 0.5


async def hello(request):
    start = time.time()
    while True:
        9 * 9
        if (time.time() - start) > DURATION:
            break
    return web.Response(text="done")


app = web.Application()
app.add_routes([web.get('/', hello)])


if __name__ == '__main__':
    web.run_app(app)
