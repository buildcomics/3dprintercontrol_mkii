#!/usr/bin/python3
""" Class to control 28-BYJ-48 Geared Stepper Motor"""
import asyncio
async def stop(board, pins):
    """set all pins low, no spurious power and current"""
    await board.digital_write(pins["motor1"], 0)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor4"], 0)


async def counterclockwise(board, pins, delay):
    """set pins to ULN2003 high in sequence from 1 to 4"""
    # 1
    await board.digital_write(pins["motor1"], 1)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor4"], 0)
    await asyncio.sleep(delay)
    # 2
    await board.digital_write(pins["motor1"], 1)
    await board.digital_write(pins["motor2"], 1)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor4"], 0)
    #delay (motor#delay);
    # 3
    await board.digital_write(pins["motor1"], 0)
    await board.digital_write(pins["motor2"], 1)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor4"], 0)
    await asyncio.sleep(delay)
    # 4
    await board.digital_write(pins["motor1"], 0)
    await board.digital_write(pins["motor2"], 1)
    await board.digital_write(pins["motor3"], 1)
    await board.digital_write(pins["motor4"], 0)
    await asyncio.sleep(delay)
    # 5
    await board.digital_write(pins["motor1"], 0)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor3"], 1)
    await board.digital_write(pins["motor4"], 0)
    await asyncio.sleep(delay)
    # 6
    await board.digital_write(pins["motor1"], 0)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor3"], 1)
    await board.digital_write(pins["motor4"], 1)
    #delay (motor#delay);
    # 7
    await board.digital_write(pins["motor1"], 0)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor4"], 1)
    await asyncio.sleep(delay)
    # 8
    await board.digital_write(pins["motor1"], 1)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor4"], 1)
    await asyncio.sleep(delay)

async def clockwise(board, pins, delay):
    """set pins to ULN2003 high in sequence from 4 to 1"""
    # 1
    await board.digital_write(pins["motor4"], 1)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor1"], 0)
    await asyncio.sleep(delay)
    # 2
    await board.digital_write(pins["motor4"], 1)
    await board.digital_write(pins["motor3"], 1)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor1"], 0)
    #delay (motor#delay);
    # 3
    await board.digital_write(pins["motor4"], 0)
    await board.digital_write(pins["motor3"], 1)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor1"], 0)
    await asyncio.sleep(delay)
    # 4
    await board.digital_write(pins["motor4"], 0)
    await board.digital_write(pins["motor3"], 1)
    await board.digital_write(pins["motor2"], 1)
    await board.digital_write(pins["motor1"], 0)
    await asyncio.sleep(delay)
    # 5
    await board.digital_write(pins["motor4"], 0)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor2"], 1)
    await board.digital_write(pins["motor1"], 0)
    await asyncio.sleep(delay)
    # 6
    await board.digital_write(pins["motor4"], 0)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor2"], 1)
    await board.digital_write(pins["motor1"], 1)
    #delay (motor#delay);
    # 7
    await board.digital_write(pins["motor4"], 0)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor1"], 1)
    await asyncio.sleep(delay)
    # 8
    await board.digital_write(pins["motor4"], 1)
    await board.digital_write(pins["motor3"], 0)
    await board.digital_write(pins["motor2"], 0)
    await board.digital_write(pins["motor1"], 1)
    await asyncio.sleep(delay)
