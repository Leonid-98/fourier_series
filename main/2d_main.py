import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QPalette
from PyQt5.QtCore import QPointF, Qt
from pyqtgraph.Qt import QtCore

from phasor_sum_visualizer import PhasorSumVisualizer
from phasor import Phasor
from sample_signals import *
from color_theme import Color

def complex_to_phasor(complex_val, freq, magnitude_divider=1):
    magnitude = np.hypot(complex_val.real, complex_val.imag) / magnitude_divider
    phase = np.angle(complex_val)
    phasor = Phasor(freq, magnitude=magnitude, phase=phase, real=complex_val.real, imaginary=complex_val.imag)

    return phasor


class Main(QWidget):
    WINDOW_WIDTH = 1080
    WINDOW_HEIGHT = 600
    G_SCALER = 1

    WAVE_MAX_LENGTH = 500
    X_POS_INCREMENT = 0

    DELTA_ANGLE = 0.005
    current_angle = 0

    path = []

    def add_point(self, point):
        qpoint = QPointF(point[0], point[1])
        self.path = [QPointF(point.x() + self.X_POS_INCREMENT, point.y()) for point in self.path]
        self.path.insert(0, qpoint)
        self.path = self.path[: self.WAVE_MAX_LENGTH]

    def drawPath(self, qp):
        for i, point in enumerate(self.path):
            if i != len(self.path) - 1:
                qp.drawLine(point, self.path[i + 1])

    def initUI(self):
        self.setGeometry(300, 300, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle("Phasors")
        pal = self.palette()

        pal.setColor(QPalette.Background, Color.background)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.show()

    def __init__(self, signal1, signal2):
        super().__init__()

        x_complex = np.fft.fft(signal1)
        self.fourier_x = [complex_to_phasor(complex_val, freq=(i + 1), magnitude_divider=len(x_complex)) for i, complex_val in enumerate(x_complex)]
        self.fourier_x = sorted(self.fourier_x, key=lambda x: x.magnitude, reverse=True)

        y_complex = np.fft.fft(signal2)
        self.fourier_y = [complex_to_phasor(complex_val, freq=(i + 1), magnitude_divider=len(y_complex)) for i, complex_val in enumerate(y_complex)]
        self.fourier_y = sorted(self.fourier_y, key=lambda y: y.magnitude, reverse=True)

        self.DELTA_ANGLE = (2 * np.pi) / len(signal1)
        self.x_psv = PhasorSumVisualizer(self, CIRCLE_START_X=540, CIRCLE_START_Y=100)
        self.x_psv.phasors = self.fourier_x

        self.y_psv = PhasorSumVisualizer(self, CIRCLE_START_X=150, CIRCLE_START_Y=360)
        self.y_psv.phasors = self.fourier_y
        self.y_psv.ROTATION_OFFSET = -np.pi / 2

        self.initUI()

    def update(self):
        self.x_psv.calculate_phasors(self.current_angle)
        self.y_psv.calculate_phasors(self.current_angle)

        if self.x_psv.x_pos != -1:
            self.add_point((self.x_psv.x_pos, self.y_psv.y_pos))

        self.current_angle += self.DELTA_ANGLE

        super().update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.x_psv.paint(qp)
        self.y_psv.paint(qp)
        qp.setPen(QPen(Color.waveform, 3))
        self.drawPath(qp)

        qp.setPen(QPen(Color.line, 3))
        qp.drawLine(int(self.y_psv.x_pos), int(self.y_psv.y_pos), int(self.x_psv.x_pos), int(self.y_psv.y_pos))
        qp.drawLine(int(self.x_psv.x_pos), int(self.x_psv.y_pos), int(self.x_psv.x_pos), int(self.y_psv.y_pos))
        qp.end()


def generate_round(scaler=200):

    t = np.linspace(0, (2 * np.pi), 100)
    signal_y = np.cos(t) * scaler
    signal_x = np.sin(t) * scaler

    return signal_x, signal_y


def main():
    app = QApplication(sys.argv)

    test_signal1, test_signal2 = generate_round()

    main = Main(signal2_x, signal2_y)
    timer = QtCore.QTimer()
    timer.timeout.connect(main.update)
    timer.start(5)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
