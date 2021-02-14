# 3D Printer Control MKII
This is the GitHub repository for the project: https://buildcomics.com/hero/3dp-gets-a-camera-arm-upgrade/ \
You will also find the "instructions"  there!

There is python3 code and a service file that controls the Arm and Power.\
python scripts for the integration with octolapse are in the Octolapse Scripts directory.

The Smoke detector and power control box are re-used from the previous arm project: https://github.com/buildcomics/3Dprintercontrol
So the powerbox schematics still apply

## Models
Find all the models for the arm and more on thingiverse: https://www.thingiverse.com/thing:4762121

## Arduino and Firmata
The arduino is programmed with Firmata Express: https://github.com/MrYsLab/FirmataExpress \


## Main Code
The main code is based on pymata express, install using pip or your favorite python installer: https://github.com/MrYsLab/pymata-express

## Wiring
All the wiring
Wiring of the arduino arm (which can be done separately) can be done using any 4 pins connected to the ULN2003A module, power is drawn via the arduino (nano) that comes in from the (powered) USB Hub. Many online good examples available, like this one: https://www.aranacorp.com/en/control-a-stepper-motor-with-arduino/ \
The pins for the Stepper Motor and limit switch are configurable in the python code.\
Schematic for the power control box in the powerbox schematic folder.

## Installation
IMPORTANT NOTE: These instructions are for my (specific) setup, you might need to change paths, filenames, adresses, ports and more to get it running for your particular setup, depending on the differences.
### 3Dprintercontrol server
You need some python packages installed on your system:
- pymata express
- octorest

Now rename or copy the config.EXAMPLE.py to config.py, and add the data for your setup.
To run the python code on your system, copy the entire folder called "3dprintercontrol"  to /srv/python.\
From there, copy the 3dprintercontrol.service file into your systemd directory of choice (mine was /lib/systemd/system/). This service file is for debian, but might need modification for your distro\
Now run it using $systemctl start 3dprintercontrol\
Optionally, enable it for auto start: systemctl enable 3dprintercontrol

### Arduino
Just upload the basic firmata express code to your arduino of choice...

### Octolapse
Copy the scripts to a directory on your octoprint/octolapse server. \
In the octolapse settings, add the printsarm_start.py/arm_stop.ph to your camera start/stop print scripts for the camera that is mounted on the arm.\
Add the script arm_move.py to the "after snapshot script".\
The other scripts can be used for testing purposes. \
You will need to install the displaylayerprogress plugin so the arm can figure out where to move to after each snapshot.

## License
MIT License

Copyright (c) 2021 buildcomics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
