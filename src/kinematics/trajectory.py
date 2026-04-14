import numpy as np

def interpolate(start, end, steps=20):
    """
    Generate a linear interpolation path between start and end points.

    Parameters:
        start : np.array — starting position [x, y, z]
        end   : np.array — ending position   [x, y, z]
        steps : int      — number of intermediate waypoints

    Returns:
        path : list of np.array waypoints from start to end
    """
    path = []
    for t in np.linspace(0, 1, steps):
        point = (1 - t) * np.array(start) + t * np.array(end)
        path.append(point)
    return path

def smooth_interpolate(start, end, steps=30):
    """
    Smooth (sinusoidal ease-in/ease-out) interpolation between two points.
    Avoids sudden jerks at the start and end of motion.

    Parameters:
        start : np.array — starting position
        end   : np.array — ending position
        steps : int      — number of waypoints

    Returns:
        path : list of np.array waypoints
    """
    path = []
    for i in range(steps):
        t = i / (steps - 1)
        t_smooth = (1 - np.cos(np.pi * t)) / 2   # sinusoidal easing
        point = (1 - t_smooth) * np.array(start) + t_smooth * np.array(end)
        path.append(point)
    return path

def multi_point_path(waypoints, steps_per_segment=20, smooth=True):
    """
    Generate a full path through multiple waypoints.

    Parameters:
        waypoints         : list of np.array positions
        steps_per_segment : steps between each consecutive pair
        smooth            : use smooth_interpolate if True, else linear

    Returns:
        full_path : list of np.array waypoints
    """
    full_path = []
    interp_fn = smooth_interpolate if smooth else interpolate

    for i in range(len(waypoints) - 1):
        segment = interp_fn(waypoints[i], waypoints[i + 1], steps=steps_per_segment)
        if i > 0:
            segment = segment[1:]   # avoid duplicating junction points
        full_path.extend(segment)

    return full_path
