import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import COLOR_RANGES

def detect_color(frame):
    """
    Detect the dominant color object in a frame.

    Parameters:
        frame : BGR image from OpenCV

    Returns:
        color    : detected color string ("RED", "GREEN", "BLUE") or None
        centroid : (cx, cy) pixel position of the detected object or None
        bbox     : (x, y, w, h) bounding box or None
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    best_color    = None
    best_centroid = None
    best_bbox     = None
    best_area     = 0

    for color, (lower, upper) in COLOR_RANGES.items():
        lower_arr = np.array(lower)
        upper_arr = np.array(upper)

        mask = cv2.inRange(hsv, lower_arr, upper_arr)

        # Morphological cleanup
        kernel = np.ones((5, 5), np.uint8)
        mask   = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
        mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500 and area > best_area:
                best_area  = area
                best_color = color

                M  = cv2.moments(cnt)
                cx = int(M['m10'] / M['m00']) if M['m00'] != 0 else 0
                cy = int(M['m01'] / M['m00']) if M['m00'] != 0 else 0
                best_centroid = (cx, cy)
                best_bbox     = cv2.boundingRect(cnt)

    return best_color, best_centroid, best_bbox

def draw_detection(frame, color, centroid, bbox):
    """
    Draw bounding box and label on frame for visualization.
    """
    if color is None or bbox is None:
        return frame

    color_map = {
        "RED":   (0, 0, 255),
        "GREEN": (0, 255, 0),
        "BLUE":  (255, 0, 0)
    }
    draw_color = color_map.get(color, (255, 255, 255))

    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)

    if centroid:
        cv2.circle(frame, centroid, 5, draw_color, -1)
        cv2.putText(frame, color, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, draw_color, 2)

    return frame
