import sys
import numpy as np
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPainter, QPen, QPalette
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from pyqtgraph.Qt import QtCore

from phasor_sum_visualizer import PhasorSumVisualizer
from phasor import Phasor
from color_theme import Color


class Main(QWidget):
    WINDOW_WIDTH = 1080
    WINDOW_HEIGHT = 480
    G_SCALER = 50

    WAVE_MAX_LENGTH = 3000
    X_POS_INCREMENT = 0.25
    X_POS_OFFSET = 450

    DELTA_ANGLE = 0.005
    nr_of_terms = 5
    waveform_nr = 0
    current_angle = 0

    path = []

    def __init__(self):
        super().__init__()
        self.psv = PhasorSumVisualizer(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle("Phasors")
        pal = self.palette()
        pal.setColor(QPalette.Background, Color.background)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        # button = QPushButton("Click me", self)
        # button.clicked.connect(self.change_waveform_nr) 
        # button.show()

        self.show()

    def change_waveform_nr(self):
        self.waveform_nr += 1
        if self.waveform_nr == 2:
            self.waveform_nr = 0
        print(self.waveform_nr)


    def update(self):
        self.psv.phasors.clear()
        self.current_angle += self.DELTA_ANGLE

        odd_freq = range(1, self.nr_of_terms * 2 + 1, 2)
        # odd_freq = range(1, self.nr_of_terms + 1)
        for freq in odd_freq:
            phasor = self.generate_waveform(freq)
            self.psv.phasors.append(phasor)

        self.psv.calculate_phasors(self.current_angle)
        if self.psv.y_pos != -1:
            self.add_point((self.X_POS_OFFSET, self.psv.y_pos))

        super().update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.psv.paint(qp)
        qp.setPen(QPen(Color.line, 3))
        self.drawPath(qp)
        qp.setPen(QPen(Color.waveform, 3))
        qp.drawLine(int(self.psv.x_pos), int(self.psv.y_pos), int(self.X_POS_OFFSET), int(self.psv.y_pos))
        qp.end()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.nr_of_terms += 1
        elif key == Qt.Key_Down and self.nr_of_terms > 0:
            self.nr_of_terms -= 1

    def add_point(self, point):
        qpoint = QPointF(point[0], point[1])
        self.path = [QPointF(point.x() + self.X_POS_INCREMENT, point.y()) for point in self.path]
        self.path.insert(0, qpoint)
        self.path = self.path[: self.WAVE_MAX_LENGTH]

    def drawPath(self, qp):
        for i, point in enumerate(self.path):
            if i != len(self.path) - 1:
                qp.drawLine(point, self.path[i + 1])

    def generate_waveform(self, n):
        if self.waveform_nr == 0:
            L = 2
            phasor = Phasor(frequency=(n * np.pi) / L, magnitude=(8 / np.pi**2) * ((-1) ** ((n - 1) / 2)) / n**2, phase=0)
        else:
            phasor = Phasor(frequency=n, magnitude=(4 / (n * np.pi)), phase=0)
        return phasor


def main():
    app = QApplication(sys.argv)
    main = Main()

    timer = QtCore.QTimer()
    timer.timeout.connect(main.update)
    timer.start(1)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
