import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from ClassificationWidget import ClassificationWidget
from FaceDetectWidget import FaceDetectWidget
from HistogramWidget import HistogramWidget
from MatplotCanvasWidget import MatplotCanvasWidget
from SegmentWidget import SegmentWidget

app = QApplication(sys.argv)

# widget = HistogramWidget()
#
# widget = SegmentWidget()

# widget = ClassificationWidget()

# widget = MatplotCanvasWidget()

widget = FaceDetectWidget()

widget.resize(1080, 640)
widget.setWindowTitle('OpenCV Demo')

widget.show()


# main_window = QMainWindow()
# # main_widget = MainWidget(haar_cascade_filepath)
# main_window.setCentralWidget(widget)
# main_window.show()


sys.exit(app.exec())
