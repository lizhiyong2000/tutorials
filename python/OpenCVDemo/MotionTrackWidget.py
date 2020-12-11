import sys
from os import path

import cv2
import numpy as np
from PIL import Image

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from motion_track_utils import detect_person_and_vehicle, box_intersection, MotionDetector

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)

    return tracker

class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_url=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_url)

        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)


class MotionTrackingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)
        self.tracking = 0
        self.motion_detector = MotionDetector()
        self.multiTracker = cv2.MultiTracker_create()


    def init_track(self, frame):

        motion, mboxes = self.motion_detector.detect(frame)
        if not motion:
            print('未检测到运动物体')
            return
        print('检测到运动物体')
        # cv2.imshow("frame", frame)
        img = Image.fromarray(frame)
        # image_path = os.path.join(ROOT_DIR, '../tests/data/image/image_car_person.jpg')
        # img = Image.open(image_path)
        # res = detect_person_and_vehicle(img)
        # if not res:
        #     print('检测接口调用失败')
        #     return
        #
        # if (not "code" in res) or res["code"] !=0:
        #     print('检测接口返回失败')
        #     return
        # # image_name_2d = "image_current.png"
        # # img.save(image_name_2d, "PNG")
        #
        # # {'code': 0, 'message': 'success', 'result': [{'box': [76, 88, 306, 298], 'label': '机动车'}, {'box': [, 68, 392, 347], 'label': '行人'}, {'box': [381, 87, 442, 108], 'label': '机动车'}, {'box': [211, 81, 276, 108], 'label'车'}, {'box': [51, 77, 85, 89], 'label': '机动车'}]}
        # detail = res['result']
        # print('检测接口调用成功:' + str(res))
        #
        # found = False
        #
        # if len(detail) > 0:
        #     found = True
        # # print(detail)
        #
        # if not found:
        #     print('未检测到检测对象')
        #     return
        #
        # detected_boxes = []
        #
        # color = (255, 255, 255)
        # for (index, item) in enumerate(detail):
        #     # self.logger.info('检测结果' + str(index))
        #     box = item['box']
        #     left, top,  right, bottom = box[0], box[1], box[2], box[3]
        #
        #     cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 1)
        #
        #     width = right - left
        #     height = bottom - top
        #
        #     if width < 30 or height < 30:
        #         continue
        #
        #     detected_boxes.append([left, top, right, bottom])
        #
        #     # draw.rectangle([(left, top), (right, bottom)], fill=None, outline=color)
        #     # draw.text((left, top), str(box), )
        #
        # # final_boxes = box_intersection(detected_boxes, mboxes)
        # final_boxes = detected_boxes.copy()

        for box in mboxes:
            if len(box) == 4:
                # trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
                # tracker = createTrackerByName('KCF')
                # self.multiTracker.add(tracker, frame, (box[0], box[1], box[2], box[3]))
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        # self.tracking = len(mboxes)

        print('开始tracking:' + str(self.tracking))

    def update_track(self, frame):
        success, boxes = self.multiTracker.update(frame)
        self.tracking = len(boxes)
        print("now tracking:" + str(self.tracking))
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)


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

        scaled_image = self.image.scaled(self.width(), self.height())
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, scaled_image)
        self.image = QtGui.QImage()




class MotionTrackWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tracking_widget = MotionTrackingWidget()

        # stream_url = "rtsp://admin:dm666666@192.168.30.224:554/h264/ch1/main/av_stream"
        # stream_url = "rtsp://admin:dp666666@192.168.10.250:554/1/1"
        stream_url = "./vlc.mp4"

        self.record_video = RecordVideo(stream_url)

        image_data_slot = self.tracking_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.tracking_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)

        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout)


