#!/usr/bin/python3
""" Class to control webcam arm """
import asyncio
import logging

async def psu_control(board, pins, loop_delay, command_queue: asyncio.Queue, logger):
    """ Main function to control the psu """
    #Set inputs and output pins
    await board.set_pin_mode_digital_input_pullup(pins["status"])
    await board.set_pin_mode_digital_output(pins["control"])
    while True:
        await asyncio.sleep(loop_delay)
        if not command_queue.empty():
            logger.debug("PSU item in queue:")
            request = command_queue.get_nowait()
            if request["type"] != "request" or not request["message"].startswith("psu."):
                logger.debug("Not of request type or not for us")
                await command_queue.put(request) #put back the message, it wasn't for us
            else:
                logger.debug("request: %s",request)
                msg = request["message"]
                answer = {
                    "type": "answer",
                    "message": "error"
                }
                if str(msg) == "psu.status": #Return the PSU status
                    psu_status = await board.digital_read(pins["status"])
                    logger.debug("PSU status requested, pin value:")
                    logger.debug(psu_status[0])
                    if not psu_status[0]:#PSU is on
                        answer["message"] = "psu.on"
                    else:
                        answer["message"] = "psu.off"
                    await command_queue.put(answer)

                elif str(msg) == "psu.on":
                    logger.debug("Turning PSU On")
                    await board.digital_write(pins["control"], 1)
                    answer["message"] = "psu.on"
                    await command_queue.put(answer)
                elif str(msg) == "psu.off":
                    logger.debug("Turning PSU Off")
                    await board.digital_write(pins["control"], 0)
                    answer["message"] = "psu.off"
                    await command_queue.put(answer)
                else:
                    logger.error("No recognized PSU request")
                    answer["message"] = "psu.error.unkonwn command"
                    await command_queue.put(answer)
