#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Our configuration is married to bluetooth.
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
# This script is modified based on Clay's original framework. Functions were added to activate and deactivate certain GPIO pins, listed below.
# Distributed under terms of the MIT license.

##This file was customized for use with a scratch built tank based on the above.

import os
import pprint
import pygame
import RPi.GPIO as GPIO
from time import sleep
import sys

#These are GPIO output addresses for each motor. If you use different pin locations on the Pi, then this will need to be adjusted.

in1 = 17 # R Motor GPIO address
#GPIO 17 = wPi , BCM 8, phys addr = 18
in2 = 27 # R Motor GPIO address
#GPIO 27 = wPi 14, BCM 11, phys addr = 16
in3 = 23 # L Motor GPIO address
#GPIO 17 = wPi 0, BCM 17, phys addr = 11
in4 = 24 # L Motor GPIO address
#GPIO 27 = wPi 2, BCM 27, phys addr = 13
en = 25 #L motor gpio for PWM
#GPIO 8 = wPi  , BCM
en2 = 22 #R MOTOR GPIO for PWM
#GPIO 22 = wPi 3, BCM 22, phys addr = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
p2=GPIO.PWM(en2,1000)

#Motor power setup here. Just one speed for now.
p.start(55)
p2.start(65) #l motor is a little weaker on my setup.
#Compensate with slightly more juice going to the weaker motor to help it drive straighter.
#With a stronger battery, turn this power level down to around 35ish to keep the DC motor speeds controllable.
#Changing these values to 100 constitutes "full send". You could break something very easily using full power depending on your setup.


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 3:
                        if event.value > 0:
                            print ("Pivot Right")
                            GPIO.output(in1,GPIO.HIGH)
                            GPIO.output(in2,GPIO.LOW)
                            GPIO.output(in3,GPIO.HIGH)
                            GPIO.output(in4,GPIO.LOW)
                        if event.value < 0:
                            print ("Pivot Left")
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.HIGH)
                            GPIO.output(in3,GPIO.LOW)
                            GPIO.output(in4,GPIO.HIGH)
                        if event.value == 0: #This function applies the brakes when the joysticks return to their base or '0' positions. Calibrate your joysticks if this value flickers from 0-1 making the motor jitter.
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.LOW)
                            GPIO.output(in3,GPIO.LOW)
                            GPIO.output(in4,GPIO.LOW)

                    if event.axis == 1:
                        if event.value > 0:
                            print ("Backwards")
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.HIGH)
                            GPIO.output(in3,GPIO.HIGH)
                            GPIO.output(in4,GPIO.LOW)
                        if event.value < 0:
                            print ("Forward")
                            GPIO.output(in1,GPIO.HIGH)
                            GPIO.output(in2,GPIO.LOW)
                            GPIO.output(in3,GPIO.LOW)
                            GPIO.output(in4,GPIO.HIGH)
                        if event.value == 0:
                            print ("stopping motors") #This function applies the brakes when the joysticks return to their base or '0' positions. Calibrate your joysticks if this value flickers from 0-1 causing motor jitters.
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.LOW)
                            GPIO.output(in3,GPIO.LOW)
                            GPIO.output(in4,GPIO.LOW)

                elif event.type == pygame.JOYBUTTONDOWN: 
                    #the action buttons area all defaulted to braking. You can configure these to do custom commands if you wish. Braking by default made the most sense.
                    if event.button == 0:
                        print("'X' Button = Stop Drive Motors")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                    if event.button == 1:
                        print("'O' Button = Stop Drive Motors")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                    if event.button == 2:
                        print("'^' Button = Stop Drive Motors")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                    if event.button == 3:
                        print("'[]' Button = Stop Drive Motors")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                    if event.button == 4:
                        print("'L1' Button = Stop L drive Motor")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                    if event.button == 5:
                        print("'R1' Button = Stop L drive Motor")
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 1:
                        print ("stopping motors") #AUTOMATIC BRAKES
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)

                elif event.type == pygame.JOYHATMOTION:
                    if event.hat == 0:
                        if event.value == (1, 0):
                            print("pivot right with directional pad")
                            GPIO.output(in1,GPIO.HIGH)
                            GPIO.output(in2,GPIO.LOW)
                            GPIO.output(in3,GPIO.HIGH)
                            GPIO.output(in4,GPIO.LOW)
                        if event.value == (-1, 0):
                            print("pivot left with directional pad")
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.HIGH)
                            GPIO.output(in3,GPIO.LOW)
                            GPIO.output(in4,GPIO.HIGH)
                        if event.value == (0, 1):
                            print("move forward with directional pad")
                            GPIO.output(in1,GPIO.HIGH)
                            GPIO.output(in2,GPIO.LOW)
                            GPIO.output(in3,GPIO.LOW)
                            GPIO.output(in4,GPIO.HIGH)
                        if event.value == (0, -1):
                            print("move reverse with directional pad")
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.HIGH)
                            GPIO.output(in3,GPIO.HIGH)
                            GPIO.output(in4,GPIO.LOW)
                        if event.value == (0, 0): #AUTOMATIC BRAKES @ '0' or center position!
                            print("brakes applied. motors stopped.")
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.LOW)
                            GPIO.output(in3,GPIO.LOW)
                            GPIO.output(in4,GPIO.LOW)


                # Insert your code on what you would like to happen for each event here!
                # In the current setup, the drive state is printing out to the screen while the motors are performing a function.
                # Brakes are defaulted to activate pretty much everywhere for safety measures. If not, the motors can run away and continue running even after the script is stopped.
                # Please do not change the braking code unless you know what you are doing or for some reason need them to keep running. 

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
