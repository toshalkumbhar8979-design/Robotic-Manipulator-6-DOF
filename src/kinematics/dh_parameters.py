import numpy as np

# DH Parameters: [theta_offset, d, a, alpha]
# Customize 'a' (link length) and 'd' (link offset) values based on your arm's physical dimensions
DH_PARAMS = [
    # [theta, d,  a,  alpha]
    [0, 10,  0,   90],   # Joint 1 — Base rotation
    [0,  0, 12,    0],   # Joint 2 — Shoulder
    [0,  0, 10,    0],   # Joint 3 — Elbow
    [0,  0,  8,   90],   # Joint 4 — Wrist pitch
    [0,  0,  0,  -90],   # Joint 5 — Wrist roll
    [0,  5,  0,    0]    # Joint 6 — Gripper
]

def dh_transform(theta, d, a, alpha):
    """
    Compute a single DH transformation matrix.
    theta : joint angle (degrees)
    d     : link offset (cm)
    a     : link length (cm)
    alpha : twist angle (degrees)
    """
    theta = np.radians(theta)
    alpha = np.radians(alpha)

    T = np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha),  np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta),  np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0,              np.sin(alpha),                   np.cos(alpha),                 d               ],
        [0,              0,                               0,                             1               ]
    ])
    return T
