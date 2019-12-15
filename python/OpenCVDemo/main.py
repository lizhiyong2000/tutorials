import sys

from PyQt5.QtWidgets import QApplication

from ClassificationWidget import ClassificationWidget
from HistogramWidget import HistogramWidget
from MatplotCanvasWidget import MatplotCanvasWidget
from SegmentWidget import SegmentWidget

app = QApplication(sys.argv)

# widget = HistogramWidget()
#
# widget = SegmentWidget()

# widget = ClassificationWidget()

widget = MatplotCanvasWidget()

widget.resize(1080, 640)
widget.setWindowTitle('OpenCV Demo')

widget.show()
sys.exit(app.exec())
