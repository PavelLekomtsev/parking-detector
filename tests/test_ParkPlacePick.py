import cv2
import numpy as np
import pickle
import pytest

from ParkingPlacePicker import rotateRectangle, mouseClick

def test_rotateRectangle():
    rect_coords1 = np.array([[0, 0], [2, 0], [0, 2], [2, 2]])
    rect_coords2 = np.array([[1, 0], [3, 0], [1, 4], [3, 4]])
    angle1, angle2 = 45, -90
    scale1, scale2 = 1.7, 2

    expected_result1 = np.array([[-1, 1], [1, -1], [1, 3], [3, 1]])
    expected_result2 = np.array([[6, 0], [6, 4], [-2, 0], [-2, 4]])

    result1 = rotateRectangle(rect_coords1, angle1, scale1)
    result2 = rotateRectangle(rect_coords2, angle2, scale2)

    assert np.allclose(result1, expected_result1)
    assert np.allclose(result2, expected_result2)

def test_mouseClick_left_button():
    events = cv2.EVENT_LBUTTONDOWN
    x, y, flags = 10, 40, 0
    params = {}

    with open("materials/CarParkPositions", "rb") as f:
        expected_list = pickle.load(f)

    expected_list.append((x, y))

    mouseClick(events, x, y, flags, params)

    with open("materials/CarParkPositions", "rb") as f:
        saved_list = pickle.load(f)

    assert saved_list == expected_list

def test_mouse_Click_right_button():
    events = cv2.EVENT_RBUTTONDOWN
    x, y, flags = 10, 40, 0
    params = {}

    with open("materials/CarParkPositions", "rb") as f:
        expected_list = pickle.load(f)

    mouseClick(events, x, y, flags, params)

    with open("materials/CarParkPositions", "rb") as f:
        saved_list = pickle.load(f)

    expected_list.pop()

    assert saved_list == expected_list