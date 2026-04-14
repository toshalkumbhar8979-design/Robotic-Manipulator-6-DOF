import numpy as np
from kinematics.dh_parameters import DH_PARAMS, dh_transform

def forward_kinematics(joint_angles):
    """
    Compute the end-effector pose from a list of 6 joint angles (degrees).

    Parameters:
        joint_angles : list of 6 float values [theta1 .. theta6]

    Returns:
        T_final : 4x4 homogeneous transformation matrix of end-effector
        position : [x, y, z] end-effector position in cm
    """
    if len(joint_angles) != 6:
        raise ValueError("Expected 6 joint angles for a 6-DOF arm.")

    T_final = np.eye(4)

    for i, (params, theta) in enumerate(zip(DH_PARAMS, joint_angles)):
        _, d, a, alpha = params
        T = dh_transform(theta, d, a, alpha)
        T_final = T_final @ T

    position = T_final[:3, 3]
    return T_final, position

def get_joint_positions(joint_angles):
    """
    Compute world-frame positions of each joint (useful for visualization).

    Returns:
        positions : list of [x, y, z] for each joint frame (7 points including base)
    """
    positions = [np.array([0.0, 0.0, 0.0])]
    T = np.eye(4)

    for i, (params, theta) in enumerate(zip(DH_PARAMS, joint_angles)):
        _, d, a, alpha = params
        T_i = dh_transform(theta, d, a, alpha)
        T = T @ T_i
        positions.append(T[:3, 3].copy())

    return positions
