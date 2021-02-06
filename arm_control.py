#!/usr/bin/python3
""" Class to control webcam arm """
import asyncio
from enum import Enum
import math
import logging
import stepper_control
from octorest import OctoRest

async def arm_control(board,pins,loop_delay,motor_delay, command_queue: asyncio.Queue, octoprint, steps, logger):
    """ Main function to control the camera arm """
    class ArmState(Enum):
        """Sate to determine state of the arm"""
        HOME = 1 #Arm in home position, Ready to start taking timelapse
        PAUSE = 2 #Paused at current position
        RUN = 3 #Running a timelapse
        MOVE = 4 #Moving to next step position (e.g. stepping)
        RETURN = 5 #Returning to home position
    current_arm_state = ArmState.RETURN
    #Set inputs and output pins
    await board.set_pin_mode_digital_input_pullup(pins["limit"])
    await board.set_pin_mode_digital_output(pins["motor1"])
    await board.set_pin_mode_digital_output(pins["motor2"])
    await board.set_pin_mode_digital_output(pins["motor3"])
    await board.set_pin_mode_digital_output(pins["motor4"])
    current_step = 0
    target_step = 0
    total_number_of_layers = 0
    steps_per_layer = 0
    while True:
        await asyncio.sleep(loop_delay)
        if not command_queue.empty():
            logger.debug("Arm item in queue:")
            request = command_queue.get_nowait()
            if request["type"] != "request" or not request["message"].startswith("arm."):
                logger.debug("Arm, message Not of request type or not of arm type")
                await command_queue.put(request) #put back the message, it wasn't for us
            else:
                logger.debug(request)
                msg = request["message"]
                answer = {
                    "type": "answer",
                    "message": "error"
                }
                if str(msg) == "arm.start": #Start rotating the arm
                    logger.debug("Arm Start Requested")
                    if current_arm_state == ArmState.HOME:#Arm is home and can be started
                        try:
                            client = OctoRest(url=octoprint["url"], apikey=octoprint["apikey"])
                            await asyncio.sleep(0.5) #Wait a bit to not overloat the octoprint API
                            layer_values=client._get('plugin/DisplayLayerProgress/values')
                            logger.debug("number of layers of current job:")
                            total_number_of_layers = layer_values["layer"]["total"]
                            logger.debug(total_number_of_layers)
                            if not total_number_of_layers.isnumeric():
                                logger.error("Nothing loaded!")
                                answer["message"] = "arm.error.could not get number of layers"
                            elif int(total_number_of_layers) > 0:
                                logger.debug("number of steps per layer:")
                                steps_per_layer = int(steps)/int(total_number_of_layers)
                                logger.debug(steps_per_layer)
                                current_step = 0
                                current_arm_state = ArmState.RUN
                                answer["message"] = "arm.running"
                            else:
                                logger.error("Layers cannot be zero!")
                                answer["message"] = "arm.error.zero layer won't work"
                        except Exception as e:
                            logger.error(e)
                            answer["message"] = "arm.error.could not connect to octoprint"
                    await command_queue.put(answer)
                elif str(msg) == "arm.move": #Perform one (between layer) movement of the arm
                    logger.debug("Arm move Requested")
                    if current_arm_state == ArmState.RUN:#Arm is actually running
                        logger.debug("Increasing target step position")
                        target_step = current_step + steps_per_layer
                        if current_step < math.floor(target_step): #if we can start moving
                            logger.debug("Time to move!")
                            current_arm_state = ArmState.MOVE
                            answer["message"] = "arm.moving"
                        else:
                            answer["message"] = "arm.moved"
                    else:
                        answer["message"] = "arm.notrunning"
                    await command_queue.put(answer)
                elif str(msg) == "arm.stop": #Time to go back home
                    logger.debug("Arm stop Requested")
                    current_arm_state = ArmState.RETURN
                    answer["message"] = "arm.returning"
                    await command_queue.put(answer)
                elif str(msg) == "arm.test": #Do a test run of the arm
                    logger.debug("Arm test run Requested")
                    if current_arm_state == ArmState.HOME:#Arm is home and can be started
                        current_step = 0
                        target_step = steps #set target step to maximum step value
                        current_arm_state = ArmState.MOVE
                        answer["message"] = "arm.moving"
                    else:
                        answer["message"] = "arm.notrunning"
                    await command_queue.put(answer)
                elif str(msg) == "arm.status": #What are we doing?
                    if current_arm_state == ArmState.HOME:#Arm is actually running
                        answer["message"] = "arm.ready"
                    elif current_arm_state == ArmState.PAUSE:
                        answer["message"] = "arm.paused"
                    elif current_arm_state == ArmState.RUN:
                        answer["message"] = "arm.running"
                    elif current_arm_state == ArmState.MOVE:
                        answer["message"] = "arm.moving"
                    elif current_arm_state == ArmState.RETURN:
                        answer["message"] = "arm.returning"
                    else:
                        answer["message"] = "arm.error.unknown state"
                    await command_queue.put(answer)
                else:
                    logger.error("No recognized ARM request")
                    answer["message"] = "arm.error.unkonwn command"
                    await command_queue.put(answer)
        if current_arm_state == ArmState.RETURN:
            limit_switch_value = await board.digital_read(pins["limit"])
            logger.debug(limit_switch_value[0])
            if limit_switch_value[0] != 1:
                await stepper_control.counterclockwise(board, pins, motor_delay)
            else:
                await stepper_control.stop(board,pins)
                current_arm_state = ArmState.HOME
                logger.debug("Arm is Ready!")
        elif current_arm_state == ArmState.MOVE: #Time to move some steps
            if current_step >= math.floor(target_step): #We have reached our designated position
                await stepper_control.stop(board,pins)
                current_arm_state = ArmState.RUN
                logger.debug("Arm is In New position")
            else:
                logger.debug("Moving arm to next target, one step at a time!")
                await stepper_control.clockwise(board, pins, motor_delay)
                current_step += 1
