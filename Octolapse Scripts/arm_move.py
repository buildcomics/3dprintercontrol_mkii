#!/usr/bin/env python3
""" script to turn on  """
import sys
import asyncio
import config as cfg

async def threedp_client(message):
    """ Send a message to 3D Printer control """
    reader, writer = await asyncio.open_connection(
        cfg.server["host"], cfg.server["port"])

    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')
    writer.close()
    if data.decode() == 'arm.moved' or data.decode() == 'arm.moving':
        exit(0)
    else:
        exit(1)
asyncio.run(threedp_client("arm.move"))
