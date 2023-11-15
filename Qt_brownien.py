import matplotlib
matplotlib.use('Qt5Agg')

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class BrownianMotionSimulation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simulation du Mouvement Brownien')
        self.setGeometry(100, 100, 800, 600)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        simulate_button = QPushButton('Simuler le Mouvement Brownien', self)
        simulate_button.clicked.connect(self.simulateBrownianMotion)
        layout.addWidget(simulate_button)

        self.setLayout(layout)

    def simulateBrownianMotion(self):
        num_steps = 1000
        dt = 0.01
        t = np.arange(0, num_steps) * dt
        x = np.cumsum(np.sqrt(dt) * np.random.normal(size=num_steps))

        self.ax.clear()
        self.ax.plot(t, x)
        self.ax.set_xlabel('Temps')
        self.ax.set_ylabel('Position')
        self.ax.set_title('Simulation du Mouvement Brownien')
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrownianMotionSimulation()
    window.show()
    sys.exit(app.exec())
