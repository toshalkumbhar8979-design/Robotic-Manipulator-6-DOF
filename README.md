# Robotic Arm 6-DOF Advanced System 🤖

An advanced end-to-end robotics framework featuring **Computer Vision**, **Inverse Kinematics (IK)**, and **Distributed Processing** across Raspberry Pi and Arduino for a 6-Degree-of-Freedom manipulator.

---

## 🏗 System Architecture
The system utilizes a distributed control architecture. The **Raspberry Pi** acts as the "Brain" for high-level computation (Vision & Math), while the **Arduino** acts as the "Nervous System" for real-time hardware execution.



### Core Functional Blocks:
1.  **Perception Layer (`vision.py`)**: Utilizes the Raspberry Pi Camera and OpenCV to detect target centroids $(x, y)$ and map them to the 3D workspace.
2.  **Kinematics Engine (`src/kinematics/`)**: 
    * **Inverse Kinematics**: Implements the Denavit-Hartenberg (DH) convention to solve for joint angles $(\theta_1 \dots \theta_6)$ required to reach a specific 3D coordinate.
    * **Forward Kinematics**: Calculates the end-effector's spatial pose to verify trajectory accuracy.
3.  **Trajectory Planner (`trajectory.py`)**: Generates smooth motion profiles to prevent mechanical vibration and ensure servo longevity.
4.  **Hardware Abstraction (`serial_control.py`)**: Orchestrates the communication protocol between the Raspberry Pi (Python) and Arduino (C++) via Serial.

---

## ✨ Key Features
* **Distributed Computing**: Offloads heavy CV and Math processing to the Raspberry Pi while maintaining low-latency PWM control on the Arduino.
* **6-DOF Precision**: Full 3D manipulation including a 3-axis spherical wrist configuration.
* **DH-Convention Modeling**: Rigorous mathematical foundation for coordinate frame transformations.
* **Real-time Computer Vision**: Optimized tracking pipeline using the Raspberry Pi Camera module.
* **Hardware Safety**: Integrated software limits and motion smoothing to prevent mechanical binding or servo stall.

---

## 🛠 Hardware Stack
* **Compute Hub**: Raspberry Pi (4B/5 recommended)
* **Controller**: Arduino Uno or Mega
* **Vision**: Raspberry Pi Camera Module
* **Actuators**: 6x MG996R / DS3218 High-Torque Servos
* **Power**: Dedicated **5V/10A DC Power Supply** (Critical: Do not power servos from the Pi or Arduino logic pins).

---

## 💻 Software Setup

### 1. Raspberry Pi Environment
Developed and tested on Raspberry Pi OS with Python 3.10+.
```bash
# Clone the repository
git clone [https://github.com/toshalkumbhar8979-design/Robotic-Manipulator-6-DOF.git]
cd robotic-arm-6dof-advanced

# Install computer vision and math dependencies
pip install -r requirements.txt

```

## 📂 Project Structure

```bash
ROBOTIC-ARM-6DOF-ADVANCED/
├── arduino/               # C++ Firmware for real-time PWM control
├── config/                # System settings and mechanical calibration
│   └── settings.py
├── docs/                  # Technical documentation and Kinematics diagrams
├── src/
│   ├── kinematics/        # Mathematical Engine (DH-Matrix, IK/FK Solvers)
│   │   ├── dh_parameters.py
│   │   ├── forward_kinematics.py
│   │   ├── inverse_kinematics.py
│   │   └── trajectory.py  # Path smoothing and interpolation
│   ├── main.py            # High-level orchestration and main loop
│   ├── serial_control.py  # Bridge between Raspberry Pi and Arduino
│   └── vision.py          # RPi Camera & OpenCV tracking logic
└── requirements.txt       # Python library dependencies

```

Authors: Toshal Kumbhar
         Soham Bhavsar

License: MIT

