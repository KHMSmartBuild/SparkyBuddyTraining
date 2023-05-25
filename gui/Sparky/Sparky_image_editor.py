
# Script name : Sparky_image_editor.py
# location = gui\Sparky_image_editor.py
# accessable from Libraries = #TODO implement libraries
# Author: KHM Smartbuild
# Purpose: TODO add this purpose
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild


import sys
from matplotlib.backend_bases import MouseEvent
import requests
from io import BytesIO
from PIL import Image
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QComboBox, QListWidget, QColorDialog, QFrame, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from .image_prompt_keywords import image_prompt_keywords


class ImageEditor(QDialog):
    def __init__(self, parent=None, image=None, keywords=None):
        super().__init__(parent)
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 800, 600)

        self.drawing = False
        self.brush_color = Qt.black
        self.brush_size = 5
        self.last_point = QPoint()

        self.grouped_keywords = {}
        self.keyword_checkbuttons = {}

        for keyword, category in image_prompt_keywords.items():
            if category not in self.grouped_keywords:
                self.grouped_keywords[category] = []
            self.grouped_keywords[category].append(keyword)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.canvas = QLabel(self)
        self.canvas.setFixedSize(800, 600)
        self.canvas.setAutoFillBackground(True)
        p = self.canvas.palette()
        p.setColor(self.canvas.backgroundRole(), Qt.white)
        self.canvas.setPalette(p)
        
        # Keyword categories
        keyword_categories_layout = QVBoxLayout()
        layout.addLayout(keyword_categories_layout)
        
        row = 0

        for keyword_category in self.grouped_keywords:
            category_label = QLabel(keyword_category, self)
            keyword_categories_layout.addWidget(category_label)
            
            checkbuttons = self.create_checkbuttons(keyword_category, row)
            self.keyword_checkbuttons[keyword_category] = checkbuttons
            keyword_categories_layout.addLayout(checkbuttons)
            row += 1


        # Set the canvas to a blank QPixmap
        self.canvas.setPixmap(QPixmap(self.canvas.size()))
        self.canvas.pixmap().fill(Qt.white)

        layout.addWidget(self.canvas)

        hbox = QHBoxLayout()

        self.pen_button = QPushButton("Pen", self)
        self.pen_button.clicked.connect(self.pen_color)
        hbox.addWidget(self.pen_button)

        self.brush_size_combo = QComboBox(self)
        for i in range(1, 21):
            self.brush_size_combo.addItem(str(i))
        self.brush_size_combo.setCurrentIndex(4)
        self.brush_size_combo.currentTextChanged.connect(self.brush_size_changed)
        hbox.addWidget(self.brush_size_combo)

        self.import_btn = QPushButton("Import Image", self)
        self.import_btn.clicked.connect(self.import_image)
        hbox.addWidget(self.import_btn)

        self.save_btn = QPushButton("Save Image", self)
        self.save_btn.clicked.connect(self.save_image)
        hbox.addWidget(self.save_btn)

        self.crop_btn = QPushButton("Crop Image", self)
        self.crop_btn.clicked.connect(self.crop_image)
        hbox.addWidget(self.crop_btn)

        self.resize_btn = QPushButton("Resize Image", self)
        self.resize_btn.clicked.connect(self.resize_image)
        hbox.addWidget(self.resize_btn)

        self.rotate_btn = QPushButton("Rotate Image", self)
        self.rotate_btn.clicked.connect(self.rotate_image)
        hbox.addWidget(self.rotate_btn)

        layout.addLayout(hbox)
        self.setLayout(layout)

        self.canvas.installEventFilter(self)

    def create_checkbuttons(self, keyword_category, row):
        checkbuttons = []
        checkbutton_layout = QHBoxLayout()

        for keyword in self.grouped_keywords[keyword_category]:
            var = QCheckBox(keyword, self)
            checkbutton_layout.addWidget(var)
            checkbuttons.append(var)

        return checkbutton_layout

    def eventFilter(self, obj, event):
        if event.type() == Qt.MouseButtonPress and obj is self.canvas:
            if self.drawing and event.buttons() == Qt.LeftButton:
                painter = QPainter(self.canvas.pixmap())
                painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.last_point, event.pos())
                self.last_point = event.pos()
                self.canvas.update()
                return True
            else:
                return super().eventFilter(obj, event)
        elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton and obj is self.canvas:
            self.last_point = event.pos()
            self.drawing = True
            return True
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton and obj is self.canvas:
            if self.drawing:
                painter = QPainter(self.canvas.pixmap())
                painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.last_point, event.pos())
                self.drawing = False
                self.canvas.update()
                return True
            else:
                return super().eventFilter(obj, event)
        else:
            return super().eventFilter(obj, event)
   
    def pen_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.brush_color = color

    def brush_size_changed(self, size):
        self.brush_size = int(size)
  
    def import_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open image', '', 'Image files (*.jpg *.gif *.png)')
        if file_name:
            image = QImage(file_name)
            self.canvas.setPixmap(QPixmap.fromImage(image))

    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save image', '', 'Image files (*.jpg *.gif *.png)')
        if file_name:
            self.canvas.pixmap().save(file_name)

    def crop_image(self):
        pass # Add crop functionality here

    def resize_image(self):
        pass # Add resize functionality here

    def rotate_image(self):
     # Add rotate functionality here
        #TODO
        pass

def main():
    app = QApplication(sys.argv)
    window = ImageEditor(keywords=image_prompt_keywords)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
