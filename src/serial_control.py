import serial
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import SERIAL_PORT, BAUD_RATE, SERVO_MIN, SERVO_MAX

ser = None

def connect():
    """Initialize serial connection to Arduino."""
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"[Serial] Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"[Serial] ERROR: Could not open port {SERIAL_PORT}. {e}")
        ser = None

def clamp_angle(angle):
    """Clamp a servo angle to the safe hardware range."""
    return max(SERVO_MIN, min(SERVO_MAX, int(angle)))

def send_angles(angles):
    """
    Send 6 joint angles to Arduino over serial.

    Parameters:
        angles : list of 6 float values (degrees)
    """
    if ser is None or not ser.is_open:
        print("[Serial] Not connected. Call connect() first.")
        return

    clamped = [clamp_angle(a) for a in angles]
    command = ','.join(map(str, clamped)) + '\n'

    ser.write(command.encode())
    print(f"[Serial] Sent: {command.strip()}")

def disconnect():
    """Close the serial connection."""
    global ser
    if ser and ser.is_open:
        ser.close()
        print("[Serial] Disconnected.")
