#!/usr/bin/python3
""" Class to control arduino using pymata express """
from pymata_express import pymata_express
class ArduinoControl():
    """Class to control Arduino using pymata with a context manager"""
    def __init__(self):
        self.ard_obj = pymata_express.PymataExpress() # instantiate pymata_express
    def __enter__(self):
        return self.ard_obj
    def __exit__(self, _x, _y, _z):
        self.ard_obj.shutdown()
