import sys
import random
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QPushButton, QColorDialog, QInputDialog, QFileDialog
)
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.class_name = 0  # Default class is 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Dataset Creator")
        self.setGeometry(100, 100, 900, 700)

        self.view = QGraphicsView(self)
        self.view.setGeometry(10, 10, 680, 680)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.points = []
        self.board_width = 680
        self.board_height = 680

        self.generate_btn = QPushButton("Generate Points", self)
        self.generate_btn.setGeometry(700, 20, 180, 30)
        self.generate_btn.clicked.connect(self.generate_points)

        self.class_btn = QPushButton("Draw Class Region", self)
        self.class_btn.setGeometry(700, 60, 180, 30)
        self.class_btn.clicked.connect(self.prepare_new_class_region)

        self.save_btn = QPushButton("Save Dataset", self)
        self.save_btn.setGeometry(700, 100, 180, 30)
        self.save_btn.clicked.connect(self.save_dataset)

        self.view.viewport().installEventFilter(self)
        self.drawing = False
        self.last_pos = None
        self.path = None
        self.current_class = None
        self.current_color = None

    def generate_points(self):
        width, ok1 = QInputDialog.getInt(self, "Board Width", "Enter board width:", value=self.board_width, min=100)
        if not ok1: return
        height, ok2 = QInputDialog.getInt(self, "Board Height", "Enter board height:", value=self.board_height, min=100)
        if not ok2: return
        count, ok3 = QInputDialog.getInt(self, "Point Count", "Enter number of points:", value=100, min=1)
        if not ok3: return

        self.board_width = width
        self.board_height = height

        self.view.setGeometry(10, 10, width, height)
        self.scene.setSceneRect(0, 0, width, height)
        self.scene.clear()
        self.points.clear()

        for _ in range(count):
            x, y = random.randint(10, width - 10), random.randint(10, height - 10)
            self.scene.addEllipse(x-2, y-2, 4, 4, QPen(), QBrush(Qt.black))
            self.points.append(Point(x, y))

    def prepare_new_class_region(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return

        label, ok = QInputDialog.getText(self, "Class Label", "Enter class name (number or string):")
        if not ok or not label:
            return

        try:
            label_val = int(label)
        except ValueError:
            try:
                label_val = float(label)
            except ValueError:
                label_val = label.strip()

        if not isinstance(label_val, (int, float, str)):
            return  # Invalid input

        self.current_class = label_val
        self.current_color = color
        self.path = QPainterPath()

    def assign_class_to_path(self):
        if self.path is None or self.current_class is None:
            return

        for p in self.points:
            if self.path.contains(QPointF(p.x, p.y)):
                p.class_name = self.current_class
                self.scene.addEllipse(p.x-3, p.y-3, 6, 6, QPen(self.current_color), QBrush(self.current_color))

        self.path = None
        self.current_class = None
        self.current_color = None

    def save_dataset(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if path:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["x", "y", "class"])
                for p in self.points:
                    writer.writerow([p.x, p.y, p.class_name])

    def eventFilter(self, source, event):
        if source == self.view.viewport():
            if event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton and self.current_class is not None:
                    self.drawing = True
                    self.last_pos = self.view.mapToScene(event.pos())
                    self.path.moveTo(self.last_pos)
            elif event.type() == event.MouseMove and self.drawing:
                new_pos = self.view.mapToScene(event.pos())
                self.scene.addLine(self.last_pos.x(), self.last_pos.y(), new_pos.x(), new_pos.y(), QPen(self.current_color, 2))
                self.path.lineTo(new_pos)
                self.last_pos = new_pos
            elif event.type() == event.MouseButtonRelease and self.drawing:
                self.drawing = False
                self.assign_class_to_path()
        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
