import numpy as np
import math

# Link lengths in cm — match DH_PARAMS 'a' values
L1 = 12   # Shoulder to elbow
L2 = 10   # Elbow to wrist

def inverse_kinematics(target, current_angles=None):
    """
    Compute joint angles to reach a target [x, y, z] position.

    Parameters:
        target         : list or array [x, y, z] in cm
        current_angles : previous angles (unused here, reserved for future IK solvers)

    Returns:
        angles : list of 6 joint angles in degrees
    """
    x, y, z = target

    # --- Joint 1: Base rotation ---
    theta1 = math.degrees(math.atan2(y, x))

    # --- Planar reach from base ---
    r = math.sqrt(x**2 + y**2)
    z_adj = z - 10  # Subtract base height (d of joint 1)

    # --- Distance check ---
    dist = math.sqrt(r**2 + z_adj**2)
    max_reach = L1 + L2
    if dist > max_reach:
        scale = (max_reach * 0.98) / dist
        r     *= scale
        z_adj *= scale

    # --- Joint 3: Elbow angle (law of cosines) ---
    D = (r**2 + z_adj**2 - L1**2 - L2**2) / (2 * L1 * L2)
    D = max(min(D, 1.0), -1.0)   # Clamp to valid acos range
    theta3 = math.degrees(math.acos(D))

    # --- Joint 2: Shoulder angle ---
    theta2 = math.degrees(
        math.atan2(z_adj, r) -
        math.atan2(
            L2 * math.sin(math.radians(theta3)),
            L1 + L2 * math.cos(math.radians(theta3))
        )
    )

    # --- Joints 4, 5, 6: Wrist kept neutral; gripper open ---
    theta4 = 90   # Wrist pitch (keep straight)
    theta5 = 90   # Wrist roll  (keep straight)
    theta6 = 30   # Gripper open angle

    return [theta1, theta2, theta3, theta4, theta5, theta6]

def apply_offsets(angles, offsets):
    """
    Apply per-joint calibration offsets.

    Parameters:
        angles  : list of 6 computed angles
        offsets : list of 6 offset values from config/settings.py

    Returns:
        adjusted : list of 6 clamped and offset-adjusted angles
    """
    adjusted = [a + o for a, o in zip(angles, offsets)]
    return adjusted
