import time

import cv2.cv2 as cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel

import matplotlib
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


class MatplotCanvasWidget(QWidget):

    def __init__(self):
        super(MatplotCanvasWidget, self).__init__()

        self.btn = QPushButton("Load Image", self)

        self.btn.clicked.connect(self.load_image)
        self.btn.resize(100, 30)
        self.btn.move(10, 10)

        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.static_canvas.setParent(self)
        self.static_canvas.resize(384, 256)
        self.static_canvas.move(10, 70)

        self._static_ax = self.static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")
        self.static_canvas.draw()

        self.dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.dynamic_canvas.setParent(self)
        self.dynamic_canvas.resize(384, 256)
        self.dynamic_canvas.move(500, 70)

        self._dynamic_ax = self.dynamic_canvas.figure.subplots()
        self._timer = self.dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()
        # self.addToolBar(QtCore.Qt.BottomToolBarArea,
        #                 NavigationToolbar(self.static_canvas, self))

        # self.creation_figure()
        # self.canvas.setParent(self)


    def load_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './images', "Image files (*.jpg *.png)")

        if len(fname) > 0:
            self.image = cv2.imread(fname)

            im_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self._static_ax.clear()
            self._static_ax.imshow(im_rgb)

            self.static_canvas.draw()




