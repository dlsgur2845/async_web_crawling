import asyncio
import sys
import time
from datetime import datetime
from functools import partial


async def wait_and_print(queue, logFile):
    while True:
        A = await queue.get()
        print(datetime.now() + " : " + A, file=logFile, flush=True)
        time.sleep(3)


def get_input(queue):
    # A = input("enter any words : ")
    A = sys.stdin.readline().strip()
    asyncio.ensure_future(queue.put(A))


async_queue = asyncio.Queue()
logFile = open("PwReset.log", "w")

loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)
loop.add_reader(sys.stdin, partial(get_input, async_queue))
loop.run_until_complete(wait_and_print(async_queue, logFile))
loop.close()
