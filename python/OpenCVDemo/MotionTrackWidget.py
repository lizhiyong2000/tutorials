import collections
import sys
from os import path

import cv2
import numpy as np
from PIL import Image

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from CVImageWidget import CVImageWidget
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
        self.camera_url = camera_url

        self.camera = None
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.camera = cv2.VideoCapture(self.camera_url)
        self.timer.start(0, self)

    def stop_recording(self):
        self.timer.stop()
        if self.camera:
            self.camera.release()

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)

class MotionDetectWidget(CVImageWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(640, 360)
        # 初始化当前帧的前两帧
        self.lastFrame1 = None
        self.lastFrame2 = None

        self.frameDelta1 = None
        self.frameDelta2 = None

        # 缓存最近5帧的结果矩形框
        self.last_frame_boxes_cache = collections.deque(maxlen=5)

    def image_data_slot(self, frame):
        # 如果第一二帧是None，对其进行初始化,计算第一二帧的不同
        if self.lastFrame2 is None:
            if self.lastFrame1 is None:
                self.lastFrame1 = frame
            else:
                self.lastFrame2 = frame
                # global frameDelta1  # 全局变量
                self.frameDelta1 = cv2.absdiff(self.lastFrame1, self.lastFrame2)  # 帧差一
            return

        mask = np.zeros(frame.shape[:2],dtype=np.uint8)

        # 计算当前帧和前帧的不同,计算三帧差分
        self.frameDelta2 = cv2.absdiff(self.lastFrame2, frame)  # 帧差二
        thresh = cv2.bitwise_and(self.frameDelta1, self.frameDelta2)  # 图像与运算

        # 当前帧设为下一帧的前帧,前帧设为下一帧的前前帧,帧差二设为帧差一
        self.lastFrame1 = self.lastFrame2
        self.lastFrame2 = frame.copy()
        self.frameDelta1 = self.frameDelta2

        # 结果转为灰度图
        thresh = cv2.cvtColor(thresh, cv2.COLOR_RGB2GRAY)
        thresh = cv2.GaussianBlur(thresh, (21, 21), 0)

        # 去除图像噪声,先腐蚀再膨胀(形态学开运算)
        thresh = cv2.dilate(thresh, None, iterations=3)
        thresh = cv2.erode(thresh, None, iterations=1)

        # 阀值图像上的轮廓位置
        cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 遍历轮廓
        for c in cnts:

            (x, y, w, h) = cv2.boundingRect(c)
            if w < 50 or h < 50:
                continue
            cv2.drawContours(mask, [c], 0, (255,255,255),1)
            # 忽略小轮廓，排除误差

        cnts, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        for c in cnts:
            # cv2.drawContours(mask, [c], 0, (255,255,0),2)
            (x, y, w, h) = cv2.boundingRect(c)
            if w < 50 or h < 50:
                continue
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 0), 2)

        self.image = self.get_qimage(mask)
        self.update()

class MotionTrackingWidget(CVImageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(640, 360)
        self.tracking = 0
        self.motion_detector = MotionDetector()
        self.multiTracker = cv2.MultiTracker_create()

    def image_data_slot(self, frame):

        self.image = self.get_qimage(frame)
        self.update()

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




class MotionTrackWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # stream_url = "rtsp://admin:dm666666@192.168.30.224:554/h264/ch1/main/av_stream"
        # stream_url = "rtsp://admin:dp666666@192.168.10.250:554/1/1"
        stream_url = "./vlc.mp4"
        self.record_video = RecordVideo(stream_url)
        self.analysing = False

        self.detect_widget = MotionDetectWidget()
        self.tracking_widget = MotionTrackingWidget()

        self.record_video.image_data.connect(self.detect_widget.image_data_slot)
        self.record_video.image_data.connect(self.tracking_widget.image_data_slot)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.detect_widget)
        layout.addWidget(self.tracking_widget)

        layout2 = QtWidgets.QVBoxLayout()

        layout2.addLayout(layout, stretch=0)

        self.run_button = QtWidgets.QPushButton('Start')
        layout2.addWidget(self.run_button)

        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout2)

    def start_analysize(self):

        if self.analysing:
            self.record_video.stop_recording()
            self.record_video.start_recording()

        # self.detect_widget.resize(640, 360)
        # self.tracking_widget.resize(640, 360)


