---
layout: post
title:  "Persistent RabbitMQ Connections and Python AsyncIO"
date: 2017-09-27 19:30:00
categories: python open-source rabbitmq asyncio heartbeat
description: Properly maintaining persistent RabbitMQ connections with Python AsyncIO
published: true
---

# Using RabbitMQ with AsyncIO

The defacto library to use with RabbitMQ with Python's AsyncIO is the
[aioamqp library](https://aioamqp.readthedocs.io/).


# Issues with persistent connections

If you have long running processes built around listening to queues and publishing
to queues, you need to make sure your connection to RabbitMQ stays open and
stable.


# RabbitMQ and heartbeat

RabbitMQ has a feature called heartbeat. The setting to tweak this is not quite
what you'd expect. In fact, if you didn't do a deep read
[into the documentation](https://www.rabbitmq.com/heartbeats.html)
on what heartbeat is doing(or if you relied on the docs from libraries), you
might think the setting meant how often a library would send heartbeats to
RabbitMQ

## Heartbeat setting explained

> The heartbeat timeout value defines after what period of time the peer TCP connection
> should be considered unreachable (down) by RabbitMQ and client libraries. This value
> is negotiated between the client and RabbitMQ server at the time of connection.


## Using heartbeats properly

If you want to do all you can to prevent connections from getting dropped by
RabbitMQ, you'll want to have a large number here.

```python

import aioamqp
transport, protocol = await aioamqp.connect(
    host, port,
    'guest', 'guest',
    heartbeat=800
)

```

## When are heartbeats issued

RabbitMQ will issue heartbeats to the server about every 2 seconds if there
is activity; however, if there is no activity, no heartbeat frames will be
sent and you could get disconnected.

However, there is a solution. You can manually send out heartbeats in an asyncio
task.

```python

import aioamqp
import asyncio


async def heartbeat(protocol):
    while True:
        await asyncio.sleep(20)  # issue manual heartbeat every 20 seconds
        await protocol.send_heartbeat()


transport, protocol = await aioamqp.connect(
    host, port,
    'guest', 'guest',
    heartbeat=800
)

asyncio.ensure_future(heartbeat(protocol))
```


# Handling other errors

Even with the heartbeat feature, you can still experience issues with disconnections
and other errors.

`aioamqp` has another feature however that allows you to do handle when any kind
of disconnect occurs. It provides a `wait_closed` coroutine, which finishes
when the connection to RabbitMQ is done.

So you can setup an asyncio task to wait for this and handle reconnects when it
comes across it.


```python

import aioamqp
import asyncio


async def handle_closed(protocol):
    await protocol.wait_closed()
    # reconnect logic here...


transport, protocol = await aioamqp.connect(
    host, port,
    'guest', 'guest',
    heartbeat=800
)

asyncio.ensure_future(handle_closed(protocol))
```
