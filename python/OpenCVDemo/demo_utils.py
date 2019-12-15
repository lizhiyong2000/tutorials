import numpy as np
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPixmap
from cv2 import cv2


def show_cvimage_to_label(image, image_label):

    #
    # print(type(image))
    #
    # print(type(image_label))

    if image.ndim == 3:
        height, width, bytes_per_component = image.shape

        format = QImage.Format_RGB888

    else:
        height, width = image.shape
        bytes_per_component = 1
        format = QImage.Format_Grayscale8

    bytes_per_line = bytes_per_component * width

    if image.ndim == 3:
        show_image = np.zeros(image.shape, np.uint8)
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB, show_image)
    else:
        show_image = image

    qimage = QImage(show_image.data, width, height, bytes_per_line, format)
    pixmap = QPixmap.fromImage(qimage)

    pixmap = pixmap.scaled(QSize(image_label.width(), image_label.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation);

    image_label.setPixmap(pixmap)
    image_label.repaint()