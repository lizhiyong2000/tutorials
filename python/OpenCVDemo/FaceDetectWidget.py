import sys
from os import path

import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)


class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath, parent=None):
        super().__init__(parent)
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)

        prototxt = "./data/opencv_face_detector.pbtxt"
        model = "./data/opencv_face_detector_uint8.pb"
        self.net = cv2.dnn.readNetFromTensorflow(model, prototxt)

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)

        return faces

    def image_data_slot(self, image_data):

        height, width, colors = image_data.shape

        # faces = self.detect_faces(image_data)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image_data,
        #                   (x, y),
        #                   (x+w, y+h),
        #                   self._red,
        #                   self._width)

        blob = cv2.dnn.blobFromImage(image_data, 1.0, (300, 300), [104., 117., 123.], False, False)
        self.net.setInput(blob)
        detections = self.net.forward()

        for i in range(0, detections.shape[2]):
            confidence = detections[0,0,i,2]
            if confidence > 0.7:
                box = detections[0,0,i,3:7] * np.array([width, height, width, height])
                (x, y, x_, y_) = box.astype("int")

                text = "{:.3f}%".format(confidence * 100)
                cy = y - 10 if x - 10 >10 else y + 10

                cv2.rectangle(image_data,  (x, y),
                                               (x_, y_),
                                               self._red,
                                               self._width)
                cv2.putText(image_data, text, (x, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)


        self.image = self.get_qimage(image_data)
        # if self.image.size() != self.size():
        #     self.setFixedSize(self.image.size())

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

        scaled_image = self.image.scaled(self.width(), self.height())
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, scaled_image)
        self.image = QtGui.QImage()


class FaceDetectWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        script_dir = path.dirname(path.realpath(__file__))
        cascade_filepath = path.join(script_dir,
                                     'data',
                                     'haarcascade_frontalface_default.xml')
        cascade_filepath = path.abspath(cascade_filepath)

        fp = cascade_filepath
        self.face_detection_widget = FaceDetectionWidget(fp)

        # TODO: set video port
        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.face_detection_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)

        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout)


