SERIAL_PORT = 'COM3'   # Change for your system (e.g., /dev/ttyUSB0)
BAUD_RATE = 9600

# Servo calibration offsets (degrees) — tune per your physical arm
SERVO_OFFSETS = [90, 90, 90, 90, 90, 30]

# Servo angle limits (hardware-safe range)
SERVO_MIN = 10
SERVO_MAX = 170

# Color detection ranges in HSV
COLOR_RANGES = {
    "RED":   [(0,  120, 70), (10, 255, 255)],
    "GREEN": [(36,  50, 70), (89, 255, 255)],
    "BLUE":  [(90,  50, 70), (128, 255, 255)]
}

# Pick and drop target positions [x, y, z] in cm
PICK_POSITION  = [15, 5, 10]
DROP_RED       = [20, 0,  10]
DROP_GREEN     = [0, 20,  10]
DROP_BLUE      = [-20, 0, 10]

# Trajectory smoothness (number of interpolation steps)
TRAJECTORY_STEPS = 20
