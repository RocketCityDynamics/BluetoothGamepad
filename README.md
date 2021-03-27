# Bluetoothgamepad.py

This script operates 2 small DC motors through RPI 3B+ GPIO pins and qty1 L298N motor controller. It enables the joysticks and buttons on a PS4 clone to operate a small tank treaded hobby vehicle with reasonable speed and safety. 

Tank treads travel backward and forward independently, creating forward or rearward movement and enabling turning.

Snippets from this script were reused in the Mycroft voice skills also listed in this repo. 

Note:  Turning action in this script is very sharp, like a pivot in place. Moving left or right is an OPPOSITE rotation of the DC drive motors, NOT a braking of one motor and running of another. The motors don't spin very fast and appear to handle the sudden reversals of direction rather easily.

There are more buttons than there are features to just the 2 DC motors. Other parts of the joystick can be coded for custom functions in this script. Action buttons default to braking. The directional pad and both joysticks drive fairly intuitively like a gently programmed RC should. The front L1/R1 triggers might be the most instinctive to use as brakes when driving.

