import base64
import collections
import json
from io import BytesIO

import cv2
import numpy as np
import requests


def image2base64(img):
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='PNG')  # 写入output_buffer
    # img.save(output_buffer, format='PNG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data = base64.b64encode(byte_data)  # 转为BASE64
    return str(base64_data, "ascii")  # 转码成功 返回base64编码

def mat_inter(box1, box2):
    """
    判断两个矩形是否相交
    box=(xA,yA,xB,yB)
    """
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = box2

    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01 - x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
        return True
    else:
        return False


def solve_coincide(box1, box2):
    """
    box=(xA,yA,xB,yB)
    计算两个矩形框的重合度
    """
    if mat_inter(box1, box2):
        x01, y01, x02, y02 = box1
        x11, y11, x12, y12 = box2
        col = min(x02, x12) - max(x01, x11)
        row = min(y02, y12) - max(y01, y11)
        intersection = col * row
        area1 = (x02 - x01) * (y02 - y01)
        area2 = (x12 - x11) * (y12 - y11)
        coincide = intersection / (area1 + area2 - intersection)
        return coincide
    else:
        return False

def box_intersection(boxes1, boxes2):
    """
    根据重合度取交集
    :param boxes1:
    :param boxes2:
    :return: 重合度。如果不重合返回False
    """
    boxes = []
    if len(boxes1) > 0 and len(boxes2) > 0:
        for bi in range(len(boxes1)):
            for bj in range(len(boxes2)):
                if len(boxes1[bi]) == 4 and len(boxes2[bj]) == 4:
                    x1, y1, x1b, y1b = int(boxes1[bi][0]), int(boxes1[bi][1]), int(boxes1[bi][2]), int(boxes1[bi][3])
                    x2, y2, x2b, y2b = int(boxes2[bj][0]), int(boxes2[bj][1]), int(boxes2[bj][2]), int(boxes2[bj][3])
                    # dis = rect_distance(x1, y1, x1b, y1b, x2, y2, x2b, y2b)

                    area1 = abs(x1b - x1) * abs(y1b - y1)
                    area2 = abs(x2b - x2) * abs(y2b - y2)

                    ratio = area1 / area2
                    if ratio > 4 or ratio < 0.25:
                        continue

                    coincide = solve_coincide((x1, y1, x1b, y1b), (x2, y2, x2b, y2b))
                    if coincide > 0.3:
                        # print("重合度：", coincide)
                        boxes.append([x1, y1, x1b, y1b])
    return boxes
def dist(x1, y1, x2, y2):
    """
    计算两点之间的距离
    input：两点坐标
    return：像素距离
    """
    distance = np.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    return distance


def rect_distance(x1, y1, x1b, y1b, x2, y2, x2b, y2b):
    """
    计算两个矩形框的距离
    input：两个矩形框，分别左上角和右下角坐标
    return：像素距离
    """
    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return dist(x1, y1b, x2b, y2)
    elif left and bottom:
        return dist(x1, y1, x2b, y2b)
    elif bottom and right:
        return dist(x1b, y1, x2, y2b)
    elif right and top:
        return dist(x1b, y1b, x2, y2)
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
    else:  # rectangles intersect
        return 0



def two2one(x1, y1, x1b, y1b, x2, y2, x2b, y2b):
    """
    将两个矩形框，变成一个更大的矩形框
    input：两个矩形框，分别左上角和右下角坐标
    return：融合后矩形框左上角和右下角坐标
    """
    x = min(x1, x2)
    y = min(y1, y2)
    xb = max(x1b, x2b)
    yb = max(y1b, y2b)
    return x, y, xb, yb


def box_select_self(boxes1):
    """
    多box，最终融合距离近的，留下新的，或未被融合的
    input：多box的列表，例如：[[12,23,45,56],[36,25,45,63],[30,25,60,35]]
    return：新的boxes，这里面返回的结果是这样的，被合并的box会置为[]，最终返回的，可能是这样[[],[],[50,23,65,50]]
    """
    if len(boxes1) > 0:
        for bi in range(len(boxes1)):
            for bj in range(len(boxes1)):
                if bi != bj:
                    if len(boxes1[bi]) == 4 and len(boxes1[bj]) == 4:
                        x1, y1, x1b, y1b = int(boxes1[bi][0]), int(boxes1[bi][1]), int(boxes1[bi][2]), int(
                            boxes1[bi][3])
                        x2, y2, x2b, y2b = int(boxes1[bj][0]), int(boxes1[bj][1]), int(boxes1[bj][2]), int(
                            boxes1[bj][3])
                        dis = rect_distance(x1, y1, x1b, y1b, x2, y2, x2b, y2b)
                        diagonal1 = dist(x1, y1, x1b, y1b)
                        diagonal2 = dist(x2, y2, x2b, y2b)
                        if dis < min(diagonal1, diagonal2):
                            # print('临近融合')
                            boxes1[bj][0], boxes1[bj][1], boxes1[bj][2], boxes1[bj][3] \
                                = two2one(x1, y1, x1b, y1b, x2, y2, x2b, y2b)
                            boxes1[bi] = []
    return boxes1

def detect_person_and_vehicle(image):
    url = 'http://36.41.71.26:8910/base/detect'
    base64_image = image2base64(image)

    request_body = {"image": base64_image}

    data = json.dumps(request_body)

    headers = {'Connection': 'close', 'content-type': "application/json"}
    try:
        resp = requests.post(url, data=data, headers=headers)
        res = json.loads(resp.content)
        # {'code': 0, 'message': 'success', 'result': [{'box': [76, 88, 306, 298], 'label': '机动车'}, {'box': [, 68, 392, 347], 'label': '行人'}, {'box': [381, 87, 442, 108], 'label': '机动车'}, {'box': [211, 81, 276, 108], 'label'车'}, {'box': [51, 77, 85, 89], 'label': '机动车'}]}
        return res
    except:
        print("检测异常")
        return None


class MotionDetector:

    def __init__(self, logger=None):

        # 初始化当前帧的前两帧
        self.lastFrame1 = None
        self.lastFrame2 = None

        self.frameDelta1 = None
        self.frameDelta2 = None

        # 缓存最近5帧的结果矩形框
        self.last_frame_boxes_cache = collections.deque(maxlen=5)
        # 缓存最近n+1帧的结果矩形框是否连续
        self.last_box_continuous_cache = collections.deque(maxlen=2)

        self.continuous_cache = []
        # 捕获到连续的结果，需要将整个过程转换GIF文件保存，作为一个告警事件
        self.frames_to_gif = []
        # 开始记录
        self.frames_to_gif_start = False
        self.gif_number = 0
        self.out_fps = 15  # 输出文件的帧率
        self.logger = logger
        pass

    def detect(self, frame):
        # 调整该帧的大小
        # frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_CUBIC)
        # 显示当前帧
        # cv2.imshow("frame", frame)

        # 如果第一二帧是None，对其进行初始化,计算第一二帧的不同
        if self.lastFrame2 is None:
            if self.lastFrame1 is None:
                self.lastFrame1 = frame
            else:
                self.lastFrame2 = frame
                # global frameDelta1  # 全局变量
                self.frameDelta1 = cv2.absdiff(self.lastFrame1, self.lastFrame2)  # 帧差一
            return False, None

        # 计算当前帧和前帧的不同,计算三帧差分
        self.frameDelta2 = cv2.absdiff(self.lastFrame2, frame)  # 帧差二
        thresh = cv2.bitwise_and(self.frameDelta1, self.frameDelta2)  # 图像与运算

        # 当前帧设为下一帧的前帧,前帧设为下一帧的前前帧,帧差二设为帧差一
        self.lastFrame1 = self.lastFrame2
        self.lastFrame2 = frame.copy()
        self.frameDelta1 = self.frameDelta2

        # 结果转为灰度图
        # thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        thresh = cv2.cvtColor(thresh, cv2.COLOR_RGB2GRAY)

        # 图像二值化
        thresh = cv2.threshold(thresh, 25, 255, cv2.THRESH_BINARY)[1]

        # 去除图像噪声,先腐蚀再膨胀(形态学开运算)
        thresh = cv2.dilate(thresh, None, iterations=3)
        thresh = cv2.erode(thresh, None, iterations=1)

        # 阀值图像上的轮廓位置
        cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # self.logger.info("{} Contours".format(len(cnts)))
        motion_detected = False
        motion_boxes = []
        # 遍历轮廓
        for c in cnts:
            # 忽略小轮廓，排除误差
            if cv2.contourArea(c) < 800:
                continue

            # 计算轮廓的边界框，在当前帧中画出该框
            (x, y, w, h) = cv2.boundingRect(c)
            if w < 30 or h < 30:
                continue
            motion_boxes.append([x, y, x + w, y + h])
            motion_detected = True
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 临近的两个矩形框融合
        box_select_self(motion_boxes)

        if motion_detected:
            return True, motion_boxes
        else:
            return False, None