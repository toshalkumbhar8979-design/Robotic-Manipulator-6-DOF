# Robotic Arm 6-DOF Advanced System 🤖

This project implements a full 6-DOF robotic arm controller using Denavit-Hartenberg (DH) parameters,
forward/inverse kinematics, trajectory planning, computer vision, and Arduino-based servo control.

## Features
- 6-DOF kinematics using DH parameters
- Forward & Inverse Kinematics
- Smooth trajectory interpolation
- OpenCV-based object detection
- Serial communication with Arduino
- Servo clamping and calibration offsets

## Hardware Required
- Arduino Uno / Mega
- 6x Servo Motors
- USB Camera / Webcam
- Robotic Arm Frame (6-DOF)
- Jumper wires + Power supply

## Software Required
- Python 3.x
- Arduino IDE

## Installation

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python src/main.py
```

## Arduino Setup
Upload `arduino/arm_6dof_advanced.ino` using Arduino IDE.

## Configuration
Edit `config/settings.py` to set:
- Serial port
- Servo offsets/limits
- Color detection ranges
- DH parameters (arm-specific)

## Important Calibration Notes
- Adjust `DH_PARAMS` in `src/kinematics/dh_parameters.py` based on your arm's link lengths
- Set `SERVO_OFFSETS` in `config/settings.py` for your physical arm
- Servo limits may not be full 0–180; adjust `SERVO_MIN` and `SERVO_MAX` accordingly

## Author
Your Name
