# Usage
# python load.py http://localhost:8080 --concurrency=100 --total=10000
import asyncio
import time
from functools import partial

import aiohttp
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('url')
parser.add_argument('--concurrency', type=int, default=100)
parser.add_argument('--total', type=int, default=10000)


class Runner:
    def __init__(self, arguments):
        self.arguments = arguments
        self.stats = {
            'start': time.time(),
            'scheduled': 0,
            'finished': 0,
            'tasks': []
        }

    async def retrieve(self, session):
        try:
            async with session.get(self.arguments.url) as resp:
                await resp.text()
                assert resp.status == 200
        except aiohttp.client_exceptions.ServerDisconnectedError:
            print('Error, server disconnected')

    def schedule(self, session):
        task = asyncio.ensure_future(self.retrieve(session))
        self.stats['scheduled'] += 1
        self.stats['tasks'].append(task)
        task.add_done_callback(partial(self.done, session))

    def done(self, session, fut):
        self.print_status()
        self.stats['tasks'].remove(fut)
        self.stats['finished'] += 1

        if self.stats['scheduled'] < self.arguments.total:
            self.schedule(session)

    async def run(self):
        conn = aiohttp.TCPConnector(limit=self.arguments.concurrency)
        async with aiohttp.ClientSession(connector=conn) as session:
            for _ in range(self.arguments.concurrency):
                self.schedule(session)

            while len(self.stats['tasks']) > 0:
                await asyncio.sleep(1)

    def print_status(self):
        if self.stats['finished'] > 0:
            now = time.time()
            secs = (now - self.stats['start'])
            per_sec = self.stats['finished'] / secs
            total_tasks = len(self.stats["tasks"])
            print(f'{self.stats["finished"]}({total_tasks}) '
                  f'- {per_sec:.2f}/req/s', end="\r")


if __name__ == '__main__':
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    runner = Runner(args)
    loop.run_until_complete(runner.run())