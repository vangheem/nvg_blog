import asyncio
import time

from aiohttp import web


DURATION = 0.5


def cpu_bound():
    start = time.time()
    while True:
        9 * 9
        if (time.time() - start) > DURATION:
            break


async def hello(request):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, cpu_bound)
    return web.Response(text="done")


app = web.Application()
app.add_routes([web.get('/', hello)])


if __name__ == '__main__':
    web.run_app(app)
