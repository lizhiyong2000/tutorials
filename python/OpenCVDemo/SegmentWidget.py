import random

import cv2.cv2 as cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel

import demo_utils


class SegmentWidget(QWidget):

    def __init__(self):
        super(SegmentWidget, self).__init__()

        self.btn = QPushButton("Load Image", self)
        self.btn.clicked.connect(self.load_image)
        self.btn.resize(100, 30)
        self.btn.move(10, 10)

        self.image_label = QLabel(self)
        self.image_label.setText("image")
        self.image_label.resize(320, 240)
        self.image_label.move(10, 50)
        self.image_label.setStyleSheet("border: 1px solid red")

        self.image = None

        self.nosie_btn = QPushButton("Remove Noise", self)
        self.nosie_btn.clicked.connect(self.remove_noise)
        self.nosie_btn.resize(120, 30)
        self.nosie_btn.move(356, 10)

        self.noise_label = QLabel(self)
        self.noise_label.setText("noise removed image")
        self.noise_label.resize(320, 240)
        self.noise_label.move(356, 50)
        self.noise_label.setStyleSheet("border: 1px solid red")

        self.light_image = None

        self.light_btn = QPushButton("Load Light", self)
        self.light_btn.clicked.connect(self.load_light_image)
        self.light_btn.resize(100, 30)
        self.light_btn.move(10, 310)

        self.light_label = QLabel(self)
        self.light_label.setText("background image")
        self.light_label.resize(320, 240)
        self.light_label.move(10, 350)
        self.light_label.setStyleSheet("border: 1px solid red")

        self.light_removed_label = QLabel(self)
        self.light_removed_label.setText("light removed image")
        self.light_removed_label.resize(320, 240)
        self.light_removed_label.move(356, 350)
        self.light_removed_label.setStyleSheet("border: 1px solid red")

        self.threshold_image = None

        self.threshold_btn = QPushButton("Threshold", self)
        self.threshold_btn.clicked.connect(self.apply_threshold)
        self.threshold_btn.resize(120, 30)
        self.threshold_btn.move(720, 10)

        self.threshold_label = QLabel(self)
        self.threshold_label.setText("threshold image")
        self.threshold_label.resize(320, 240)
        self.threshold_label.move(720, 50)
        self.threshold_label.setStyleSheet("border: 1px solid red")

        self.segment_label = QLabel(self)
        self.segment_label.setText("segmented image")
        self.segment_label.resize(320, 240)
        self.segment_label.move(720, 350)
        self.segment_label.setStyleSheet("border: 1px solid red")

    def load_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './images', "Image files (*.jpg *.png *.pgm)")

        if len(fname) > 0:
            self.image = cv2.imread(fname)
            # cv2.imshow(fname, image)
            demo_utils.show_cvimage_to_label(self.image, self.image_label)

            self.remove_noise()

    def load_light_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './images', "Image files (*.jpg *.png *.pgm)")

        if len(fname) > 0:
            self.light_image = cv2.imread(fname)
            # cv2.imshow(fname, image)
            demo_utils.show_cvimage_to_label(self.light_image, self.light_label)

            self.remove_light()

    def remove_noise(self):

        height, width, bytes_per_component = self.image.shape
        bytes_per_line = 3 * width

        self.noise_image = np.zeros(self.image.shape, np.uint8)

        cv2.medianBlur(self.image, 3, self.noise_image)

        demo_utils.show_cvimage_to_label(self.noise_image, self.noise_label)

    def remove_light(self):

        height, width, bytes_per_component = self.image.shape
        bytes_per_line = 3 * width

        img32 = np.float32(self.noise_image)
        light32 = np.float32(self.light_image)
        #
        devided = np.divide(img32, light32)

        sub_result = 1 - devided

        aux = abs(255 * sub_result)
        self.light_removed_image = np.uint8(aux)

        # light_removed_image = abs(light32 - img32)
        # light_removed_image = np.uint8(light_removed_image)

        # light_removed_image = np.zeros(self.image.shape, np.uint8)
        # cv2.medianBlur(self.image, 3, light_removed_image)

        demo_utils.show_cvimage_to_label(self.light_removed_image, self.light_removed_label)

    def apply_threshold(self):

        height, width, bytes_per_component = self.image.shape
        bytes_per_line = 3 * width

        self.threshold_image = np.zeros(self.image.shape, np.uint8)
        cv2.threshold(self.light_removed_image, 50, 255, cv2.THRESH_BINARY, self.threshold_image)

        demo_utils.show_cvimage_to_label(self.threshold_image, self.threshold_label)

        imgray = cv2.cvtColor(self.threshold_image, cv2.COLOR_BGR2GRAY)

        result = cv2.connectedComponentsWithStats(imgray)

        # cv2.CC_STAT_AREA

        print(" %d objects found" % result[0])
        num_labels = result[0]
        # The second cell is the label matrix
        labels = result[1]
        stats = result[2]
        controlids = result[3]

        output = np.zeros(self.image.shape, np.uint8)

        random.seed()

        font = cv2.FONT_HERSHEY_SIMPLEX

        # org
        org = (50, 50)

        # fontScale
        fontScale = 0.5

        # Blue color in BGR
        color1 = (255, 0, 0)

        # Line thickness of 2 px
        thickness = 1

        outputed = False
        for i in range(1, num_labels):
            area = stats[i][cv2.CC_STAT_AREA]
            if area > 10:
                print("object:%d with area %d" % (i, area))
                mask = labels == i

                color = (random.randint(40, 220), random.randint(40, 220), random.randint(40, 220))

                # np.putmask(output, mask, [color])

                output[mask] = color

                # Using cv2.putText() method

                # if not outputed:

                print(controlids[i])

                org = controlids[i].astype(int)

                output = cv2.putText(output, "area: %d" % (area), tuple(org), font,
                                     fontScale, color, thickness)

                # outputed = True
                # cv2.putText(output, "area %d" % (area), tuple(controlids[i]), cv2.FONT_HERSHEY_COMPLEX,int(6) , color)
        demo_utils.show_cvimage_to_label(output, self.segment_label)
