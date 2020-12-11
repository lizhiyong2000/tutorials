import cv2
import numpy as np
from PIL import Image

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

class CVImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)

    def image_data_slot(self, frame):

        height, width, colors = frame.shape
        if self.tracking == 0:
            self.init_track(frame)
        else:
            self.update_track(frame)

        self.image = self.get_qimage(frame)
        self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        # print("%d, %d" % (self.width(), self.height()))
        scaled_image = self.image.scaled(self.width(), self.height())
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, scaled_image)
        self.image = QtGui.QImage()
