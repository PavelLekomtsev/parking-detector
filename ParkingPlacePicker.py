import cv2
import numpy as np
import pickle

def loadPositionList():
    """
    Загружает список позиций из файла в формате pickle.

    Returns:
    position_list (list): Список загруженных позиций либо пустой список, если файл не найден.
    """
    try:
        with open("materials/CarParkPositions", "rb") as f:
            position_list = pickle.load(f)
    except FileNotFoundError:
        position_list = []
    return position_list

def savePositionList(position_list):
    """
    Сохраняет список позиций в файл "CarParkPositions" в формате pickle.

    Args:
    position_list (list): Список позиций для сохранения.
    """
    with open("materials/CarParkPositions", "wb") as f:
        pickle.dump(position_list, f)

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

def mouseClick(events, x, y, flags, params):
    """
    Обработчик событий мыши для разметки парковочных мест на изображении.

    Args:
    events: тип события, связанного с мышью.
    x: координата x точки, на которую произошёл клик мыши.
    y: координата y точки, на которую произощёл клик мыши.
    flags: дополнительные флаги события мыши.
    params: дополнительные параметры для обработки событий.

    Returns:
    Сохраняет обновлённый список парковочных мест в файл CarParkPositions
    """
    if events == cv2.EVENT_LBUTTONDOWN:
        position_list.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(position_list):
            x1, y1 = pos
            if x1 <= x < x1 + width and y1 <= y < y1 + height:
                position_list.pop(i)

    savePositionList(position_list)

def drawRotatedRectangle(img, new_rectangle):
    """
    Отрисовывает повернутый прямоугольник на изображении.

    Args:
    img (numpy.ndarray): Изображение, на котором будет отрисован прямоугольник.
    new_rectangle (numpy.ndarray): Координаты точек повернутого прямоугольника.

    Returns:
    None
    """
    for i in range(4):
        cv2.line(img, (int(new_rectangle[i][0]), int(new_rectangle[i][1])),
                 (int(new_rectangle[(i + 1) % 4][0]), int(new_rectangle[(i + 1) % 4][1])), (255, 0, 255), 2)

if __name__ == "__main__":
    position_list = loadPositionList()
    borders = (930, 480)
    width, height = 95, 40

    while True:
        img = cv2.imread("materials/ParkPhoto.png")

        for pos in position_list:
            if pos[0] < borders[0]:
                # rule 1
                angle, scale = -11, 0.7
                height_offset, width_offset = int(pos[1]/50) + 4, - 5 - (pos[1]-borders[1])//14
            elif pos[0] >= borders[0] and pos[1] > borders[1]:
                # rule 2
                angle, scale = -1, 0.8
                height_offset, width_offset = int(pos[1]/40), 10
            else:
                # rule 3
                angle, scale = 93, 1
                height_offset, width_offset = 20, 65

            rect_coords = np.array([[pos[0], pos[1]], [pos[0] + width - width_offset, pos[1]],
                                    [pos[0] + width - width_offset, pos[1] + height - height_offset],
                                    [pos[0], pos[1] + height - height_offset]])
            new_rectangle = rotateRectangle(rect_coords, angle, scale)

            drawRotatedRectangle(img, new_rectangle)

        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", mouseClick)
        key = cv2.waitKey(1)
        if key == ord('r'):
            cv2.destroyAllWindows()
            break