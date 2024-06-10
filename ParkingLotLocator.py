import cv2
import pickle
import cvzone
import numpy as np

with open("materials/CarParkPositions", "rb") as f:
    position_list = pickle.load(f)

def rotateRectangle(rect_coords, angle, scale):
    """
    Поворачивает прямоугольник с координатами rect_coords на заданный угол angle
    и масштабирует его на величину scale.

    Args:
    rect_coords (numpy.array): Координаты вершин прямоугольника.
    angle (int): Угол поворота прямоугольника в градусах.
    scale (float): Масштабирование прямоугольника.

    Returns:
    numpy.array: Новые координаты вершин повёрнутого и масштабированного прямоугольника
    """
    center_x = np.mean(rect_coords[:, 0])
    center_y = np.mean(rect_coords[:, 1])

    matrix_rotation = cv2.getRotationMatrix2D((center_x, center_y), angle, scale)
    new_rect = cv2.transform(np.array([rect_coords]), matrix_rotation)[0]
    return new_rect

def checkParkingSpace(imgProcess):
    """
    Обрабатывает изображение и определяет количество доступных парковочных мест.

    Args:
    imgProcess (numpy.ndarray)

    Returns:
    Отображаются границы парковочных мест различными цветами и толщинами, выводится
    вспомогательная информация о количестве парковочных мест на изображении.
    """
    space_counter = 0

    for pos in position_list:
        x, y = pos
        if pos[0] < borders[0]:
            # rule 1
            angle, scale = -11, 0.7
            height_offset, width_offset = 15 - (pos[1]-borders[1])//15, - 5 - (pos[1]-borders[1])//14
        elif pos[0] >= borders[0] and pos[1] > borders[1]:
            # rule 2
            angle = -1
            scale = 0.8
            height_offset, width_offset = 20 - (pos[1]-borders[1])//15, 20 - (pos[1]-borders[1])//14
        else:
            # rule 3
            angle = 93
            scale = 1
            height_offset, width_offset = 20, 65

        imgCrop = imgProcess[y:y + height - height_offset, x:x + width - width_offset]
        count = cv2.countNonZero(imgCrop)

        if pos[0] < borders[0]:
            if pos[0] < borders[0] and pos[1] <= borders[2] and count < 900:
                space_counter += 1
                color = (0, 255, 0)
                thickness = 3
            elif pos[0] < borders[0] and pos[1] > borders[2] and count < 1050:
                space_counter += 1
                color = (0, 255, 0)
                thickness = 3
            else:
                color = (0, 0, 255)
                thickness = 2
        elif pos[0] >= borders[0] and pos[1] > borders[1]:
            if count < 510:
                space_counter += 1
                color = (0, 255, 0)
                thickness = 3
            else:
                color = (0, 0, 255)
                thickness = 2
        else:
            if count < 90:
                space_counter += 1
                color = (0, 255, 0)
                thickness = 3
            else:
                color = (0, 0, 255)
                thickness = 2

        rect_coords = np.array([[pos[0], pos[1]], [pos[0] + width - width_offset, pos[1]],
                                [pos[0] + width - width_offset, pos[1] + height - height_offset],
                                [pos[0], pos[1] + height - height_offset]])
        new_rectangle = rotateRectangle(rect_coords, angle, scale)

        for i in range(4):
            cv2.line(img, (int(new_rectangle[i][0]), int(new_rectangle[i][1])),
                     (int(new_rectangle[(i + 1) % 4][0]), int(new_rectangle[(i + 1) % 4][1])), color, thickness)

        cvzone.putTextRect(img, str(count), (x, y + height - height_offset - 8), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {space_counter}/{len(position_list)}', (1000, 50), scale=2,
                       thickness=3, offset=10, colorR=(0, 200, 0))


cap = cv2.VideoCapture("materials/ParkVideo.mp4")
borders = (930, 475, 530)
width, height = 95, 40

while True:
    success, img = cap.read()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 12)
    img_median = cv2.medianBlur(img_threshold, 3)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations = 1)

    checkParkingSpace(img_dilate)

    cv2.imshow("Video", img)
    # cv2.imshow("Image Blur", img_blur)
    # cv2.imshow("Image Threshhold", img_dilate)
    key = cv2.waitKey(10)
    if key == ord('r'):
        cv2.destroyAllWindows()
        break