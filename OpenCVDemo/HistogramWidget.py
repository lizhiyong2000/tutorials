import cv2.cv2 as cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel

import demo_utils


class HistogramWidget(QWidget):

    def __init__(self):
        super(HistogramWidget, self).__init__()

        self.btn = QPushButton("Load Image", self)

        self.btn.clicked.connect(self.load_image)
        self.btn.resize(100, 30)
        self.btn.move(10, 10)

        self.image_label = QLabel(self)
        self.image_label.setText("image")
        self.image_label.resize(256, 256)
        self.image_label.move(10, 50)
        self.image_label.setStyleSheet("border: 1px solid red")

        self.image = None

        self.histogram_btn = QPushButton("Histogram", self)
        self.histogram_btn.clicked.connect(self.show_histogram)
        self.histogram_btn.resize(100, 30)
        self.histogram_btn.move(286, 10)

        self.histogram_label = QLabel(self)
        self.histogram_label.setText("histogram")
        self.histogram_label.resize(256, 256)
        self.histogram_label.move(286, 50)
        self.histogram_label.setStyleSheet("border: 1px solid red")

        self.histogram_label2 = QLabel(self)
        self.histogram_label2.setText("histogram")
        self.histogram_label2.resize(256, 256)
        self.histogram_label2.move(552, 50)
        self.histogram_label2.setStyleSheet("border: 1px solid red")

        self.gray_btn = QPushButton("Load Gray Image", self)

        self.gray_btn.clicked.connect(self.load_gray_image)
        self.gray_btn.resize(150, 30)
        self.gray_btn.move(10, 330)

        self.gray_image_label = QLabel(self)
        self.gray_image_label.setText("image")
        self.gray_image_label.resize(256, 256)
        self.gray_image_label.move(10, 360)
        self.gray_image_label.setStyleSheet("border: 1px solid red")

        self.gray_image = None

        self.gray_histogram_btn = QPushButton("Gray Histogram", self)
        # self.gray_histogram_btn.clicked.connect(self.show_gray_histogram)
        self.gray_histogram_btn.resize(150, 30)
        self.gray_histogram_btn.move(286, 330)

        self.gray_histogram_label = QLabel(self)
        self.gray_histogram_label.setText("gray histogram")
        self.gray_histogram_label.resize(256, 256)
        self.gray_histogram_label.move(286, 360)
        self.gray_histogram_label.setStyleSheet("border: 1px solid red")

    def load_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './images', "Image files (*.jpg *.png)")

        if len(fname) > 0:
            self.image = cv2.imread(fname)
            # cv2.imshow(fname, image)
            demo_utils.show_cvimage_to_label(self.image, self.image_label)
            self.show_histogram()

    def show_histogram(self):
        # hist = cv2.calcHist([self.image],
        #                     [0], #使用的通道
        #                     None, #没有使用mask
        #                     [256], #HistSize
        #                     [0.0,255.0])

        b, g, r = cv2.split(self.image)
        numbins = 256
        ranges = [0.0, 256.0]

        b_hist = cv2.calcHist([b], [0], None, [numbins], ranges)
        g_hist = cv2.calcHist([g], [0], None, [numbins], ranges)
        r_hist = cv2.calcHist([r], [0], None, [numbins], ranges)

        print(b_hist.shape)

        width = 256
        height = 256

        hist_image = np.zeros([height, width, 3], np.uint8)

        cv2.normalize(b_hist, b_hist, 0, height * 0.9, cv2.NORM_MINMAX)
        cv2.normalize(g_hist, g_hist, 0, height * 0.9, cv2.NORM_MINMAX)
        cv2.normalize(r_hist, r_hist, 0, height * 0.9, cv2.NORM_MINMAX)

        for i in range(1, numbins, 1):
            cv2.line(hist_image,
                     (i - 1, height - np.int32(np.around(b_hist[i - 1][0]))),
                     (i, height - np.int32(np.around(b_hist[i][0]))),
                     (255, 0, 0)
                     )
            cv2.line(hist_image,
                     (i - 1, height - np.int32(np.around(g_hist[i - 1][0]))),
                     (i, height - np.int32(np.around(g_hist[i][0]))),
                     (0, 255, 0)
                     )
            cv2.line(hist_image,
                     (i - 1, height - np.int32(np.around(r_hist[i - 1][0]))),
                     (i, height - np.int32(np.around(r_hist[i][0]))),
                     (0, 0, 255)
                     )

        # cv2.imshow("Histogram", hist_image)
        demo_utils.show_cvimage_to_label(hist_image, self.histogram_label)

        self.show_histogram2()

    def show_histogram2(self):
        # hist = cv2.calcHist([self.image],
        #                     [0], #使用的通道
        #                     None, #没有使用mask
        #                     [256], #HistSize
        #                     [0.0,255.0])

        # b, g, r = cv2.split(self.image)
        numbins = 256
        ranges = [0.0, 255.0]

        width = 256
        height = 256

        bytes_per_line = 3 * width

        hist_image = np.zeros([height, width, 3], np.uint8)

        # hist_image = np.zeros((256,256,3)) #创建用于绘制直方图的全0图像

        bins = np.arange(numbins).reshape(numbins, 1)  # 直方图中各bin的顶点位置

        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # BGR三种颜色

        for ch, col in enumerate(color):
            origin_hist = cv2.calcHist([self.image], [ch], None, [numbins], ranges)
            cv2.normalize(origin_hist, origin_hist, 0, 255 * 0.9, cv2.NORM_MINMAX)
            hist = np.int32(np.around(origin_hist))
            pts = np.column_stack((bins, hist))
            cv2.polylines(hist_image, [pts], False, col)

        # print(type(hist_image.data))

        hist_image = np.flipud(hist_image)
        demo_utils.show_cvimage_to_label(hist_image, self.histogram_label2)

    def load_gray_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './images', "Image files (*.jpg *.png)")

        if len(fname) > 0:
            self.gray_image = cv2.imread(fname)
            # cv2.imshow(fname, image)

            demo_utils.show_cvimage_to_label(self.gray_image, self.gray_image_label)

            self.show_gray_histogram()

    def show_gray_histogram(self):
        numbins = 256
        ranges = [0.0, 255.0]

        width = 256
        height = 256

        bytes_per_line = 3 * width

        hist_image = np.zeros([height, width, 3], np.uint8)

        # hist_image = np.zeros((256,256,3)) #创建用于绘制直方图的全0图像

        bins = np.arange(numbins).reshape(numbins, 1)  # 直方图中各bin的顶点位置

        color = [(255, 0, 0)]  # BGR三种颜色

        for ch, col in enumerate(color):
            origin_hist = cv2.calcHist([self.gray_image], [ch], None, [numbins], ranges)
            cv2.normalize(origin_hist, origin_hist, 0, 255 * 0.9, cv2.NORM_MINMAX)
            hist = np.int32(np.around(origin_hist))
            pts = np.column_stack((bins, hist))
            cv2.polylines(hist_image, [pts], False, col)

        # print(type(hist_image.data))
        hist_image = np.flipud(hist_image)
        # cv2.imshow("histogram", hist_image)
        demo_utils.show_cvimage_to_label(hist_image, self.gray_histogram_label)
