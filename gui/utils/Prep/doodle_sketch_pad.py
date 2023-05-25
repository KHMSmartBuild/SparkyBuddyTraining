from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QPoint, QRect
import os
import tempfile

class DoodleSketchPad(QGraphicsView):
    def __init__(self, parent=None, image=None, keywords=None, touchscreen=False):
        super().__init__(parent)
        self.touchscreen = touchscreen
        self.initUI()

    def initUI(self):
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.lastPoint = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            if self.touchscreen:
                if event.source() == Qt.MouseEventSynthesizedBySystem:
                    print("Touch move event")
            else:
                print("Mouse move event")
            
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def get_doodle(self):
        return self.image
    
    def save_doodle(self, file_name=None):
        if not file_name:
            temp_dir = tempfile.gettempdir()
            file_name = os.path.join(temp_dir, "doodle.png")
        self.image.save(file_name)
        return file_name