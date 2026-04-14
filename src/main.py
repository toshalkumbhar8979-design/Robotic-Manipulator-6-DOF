import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from kinematics.inverse_kinematics import inverse_kinematics, apply_offsets
from kinematics.trajectory import smooth_interpolate
from vision import detect_color, draw_detection
from serial_control import connect, send_angles, disconnect
from config.settings import (
    SERVO_OFFSETS, TRAJECTORY_STEPS,
    PICK_POSITION, DROP_RED, DROP_GREEN, DROP_BLUE
)

# Initial arm pose (all joints at neutral)
current_angles = [90, 90, 90, 90, 90, 30]

def move_to(target_xyz):
    """
    Move end-effector smoothly to target [x, y, z] using trajectory + IK.
    """
    global current_angles

    current_pos = np.array(current_angles[:3], dtype=float)
    target_pos  = np.array(target_xyz, dtype=float)

    path = smooth_interpolate(current_pos, target_pos, steps=TRAJECTORY_STEPS)

    for point in path:
        angles = inverse_kinematics(point, current_angles)
        angles = apply_offsets(angles, SERVO_OFFSETS)
        send_angles(angles)
        current_angles = angles

def run_vision_loop():
    """
    Main camera loop: detects colored objects and triggers sort movement.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[Vision] ERROR: Cannot open camera.")
        return

    print("[Vision] Camera started. Press ESC to quit.")

    DROP_MAP = {
        "RED":   DROP_RED,
        "GREEN": DROP_GREEN,
        "BLUE":  DROP_BLUE
    }

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Vision] Frame capture failed.")
            break

        color, centroid, bbox = detect_color(frame)
        frame = draw_detection(frame, color, centroid, bbox)

        if color:
            print(f"[Vision] Detected: {color}")
            move_to(PICK_POSITION)
            move_to(DROP_MAP[color])

        cv2.imshow("Robotic Arm — 6DOF Vision", frame)

        if cv2.waitKey(1) & 0xFF == 27:   # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    connect()
    try:
        run_vision_loop()
    finally:
        disconnect()
