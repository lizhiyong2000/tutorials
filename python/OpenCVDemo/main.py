import sys
import cv2

from PyQt5.QtWidgets import QApplication, QMainWindow

from ClassificationWidget import ClassificationWidget
from FaceDetectWidget import FaceDetectWidget
from HistogramWidget import HistogramWidget
from MatplotCanvasWidget import MatplotCanvasWidget
from MotionTrackWidget import MotionTrackWidget
from SegmentWidget import SegmentWidget

# print(cv2.getBuildInformation())

app = QApplication(sys.argv)

# widget = HistogramWidget()
#
# widget = SegmentWidget()

# widget = ClassificationWidget()

# widget = MatplotCanvasWidget()

# widget = FaceDetectWidget()


widget = MotionTrackWidget()


widget.resize(1080, 640)
widget.setWindowTitle('OpenCV Demo')

widget.show()


# main_window = QMainWindow()
# # main_widget = MainWidget(haar_cascade_filepath)
# main_window.setCentralWidget(widget)
# main_window.show()


sys.exit(app.exec())
