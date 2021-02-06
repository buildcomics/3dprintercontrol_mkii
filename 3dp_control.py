#!/usr/bin/python3
"""
    Script to control Webcam Camera Orbitor for octolapse plugin for octoprint
    AND the psucontrol plugin
    For octoprint servers that do not have their own I/O
    This program uses an arduino (nano) with firmata-express
    """
import asyncio
#import time
import sys
import argparse
import logging
import arduino_control
import arm_control
import psu_control
import config as cfg

command_queue = asyncio.Queue()

async def handle_client(reader, writer):
    """ Handle client connections """
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    logger.debug("Received %s from %s", message,addr)
    request = {
        "type": "request",
        "message": message
    }
    if message.startswith("arm.") or message.startswith("psu."):
        await command_queue.put(request)
        logger.debug("sending request:")
        logger.debug(request)
        logger.debug("waiting for answer...")
        while True:
            await asyncio.sleep(0.01)
            if not command_queue.empty():
                logger.debug("Client: Item in queue:")
                answer = command_queue.get_nowait()
                logger.debug(answer)
                if answer["type"] != "answer":
                    logger.debug("Not of answer type")
                    await command_queue.put(answer) #put back the message, it wasn't for us
                else:
                    logger.debug("received answer")
                    logger.debug(answer)
                    msg = answer["message"]
                    logger.debug("Send: %s", msg)
                    writer.write(msg.encode())
                    await writer.drain()
                    logger.debug("Close the connection")
                    writer.close()
                    break
    else:
        logging.error("Unknwon message type")
        msg = "error.unknown message type"
        logger.debug("Send: %s", msg)
        writer.write(msg.encode())
        await writer.drain()
        logger.debug("Close the connection")
        writer.close()

async def main():
    """ Main function to run """
    server = await asyncio.start_server(
        handle_client, cfg.server["host"], cfg.server["port"])

    addr = server.sockets[0].getsockname()
    logger.info("Serving on %s",addr)

    async with server:
        #await server.serve_forever()
        await asyncio.gather(server.serve_forever(),
                            psu_control.psu_control(arduino,
                                                    psu_pins,
                                                    cfg.psu["loop_delay"],
                                                    command_queue,
                                                    logger),
                            arm_control.arm_control(arduino,
                                                        arm_pins,
                                                        cfg.arm["loop_delay"],
                                                        cfg.arm["motor_delay"],
                                                        command_queue,
                                                        cfg.octoprint,
                                                        cfg.arm["pan_steps"],
                                                        logger)
                                                    )
parser = argparse.ArgumentParser(
    description='3D Printer Control for Power Supply and Webcam Arm'
)
parser.add_argument("-v", "--verbose", help="Set Debug Mode Logging",
                    action="store_true")
logger = logging.getLogger("3D Printer Control Daemon")
logging.basicConfig(format='%(asctime)s %(message)s')
args = parser.parse_args()
if args.verbose:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARNING)

logger.debug('Starting up!')

loop = asyncio.get_event_loop()# get the event loop
with arduino_control.ArduinoControl() as arduino:
    logger.info("opened arduino!")
    arm_pins = {
        "motor1": cfg.arm["stepper_pin1"],
        "motor2": cfg.arm["stepper_pin2"],
        "motor3": cfg.arm["stepper_pin3"],
        "motor4": cfg.arm["stepper_pin4"],
        "limit" : cfg.arm["limitswitch_pin"]
    }
    psu_pins = {
        "status": cfg.psu["readout_pin"],
        "control": cfg.psu["control_pin"]
    }
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, RuntimeError) as e:
        loop.run_until_complete(arduino.shutdown())
        sys.exit(0)
