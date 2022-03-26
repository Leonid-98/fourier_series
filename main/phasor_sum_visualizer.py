from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QWidget
import numpy as np
from color_theme import Color

class PhasorSumVisualizer(QWidget):
    def __init__(self, parent, CIRCLE_START_X=250, CIRCLE_START_Y=250) -> None:
        super().__init__(parent=parent)
        self.G_SCALER = parent.G_SCALER
        self.CIRCLE_START_X = CIRCLE_START_X
        self.CIRCLE_START_Y = CIRCLE_START_Y
        self.ROTATION_OFFSET = 0

        self.x_pos = CIRCLE_START_X
        self.y_pos = CIRCLE_START_Y

        self.phasors = []
        self.circles = []

    def calculate_phasors(self, angle):
        self.circles.clear()
        for phasor in self.phasors:
            r = phasor.magnitude * self.G_SCALER
            theta = -phasor.frequency * angle - phasor.phase + self.ROTATION_OFFSET

            x_pos = r * np.cos(theta)
            y_pos = -r * np.sin(theta)

            self.circles.append([[x_pos, y_pos], r])

    def paint(self, qp):
        qp.setPen(QPen(Color.circle, 3))
        qp.drawEllipse(QPointF(self.CIRCLE_START_X, self.CIRCLE_START_Y), 4, 4)

        x_pos, y_pos = -1, -1
        prev_middle_x, prev_middle_y = self.CIRCLE_START_X, self.CIRCLE_START_Y
        for circle in self.circles:
            x_pos = circle[0][0] + prev_middle_x
            y_pos = circle[0][1] + prev_middle_y
            radius = circle[1]

            qp.drawEllipse(QPointF(prev_middle_x, prev_middle_y), radius, radius)
            qp.drawLine(prev_middle_x, prev_middle_y, x_pos, y_pos)

            prev_middle_x, prev_middle_y = x_pos, y_pos

        self.y_pos = y_pos
        self.x_pos = x_pos
