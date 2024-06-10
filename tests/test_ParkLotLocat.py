import cv2
import numpy as np
import pytest

from ParkingLotLocator import checkParkingSpace

def test_checkParkingSpace():
    img = cv2.imread("materials/ParkPhoto.png")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 23, 11)
    # Убираем медианный блюринг
    # img_median = cv2.medianBlur(img_threshold, 3)
    kernel = np.ones((4, 4), np.uint8)
    img_dilate = cv2.dilate(img_threshold, kernel, iterations=2)

    result = checkParkingSpace(img_dilate)

    assert result is None