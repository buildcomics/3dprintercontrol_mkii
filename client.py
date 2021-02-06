#!/usr/bin/python3
""" script to control 3dp control """
import sys
import asyncio
import config as cfg

async def threedp_client(message):
    """ Send a message to 3D Printer control """
    reader, writer = await asyncio.open_connection(
        cfg.server["host"], cfg.server["port"])

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    writer.close()
if len(sys.argv) != 2:
    print("Call this function with ONE parameter, like ./" + str(sys.argv[0]) + " start")
else:
    asyncio.run(threedp_client(str(sys.argv[1])))
