import matplotlib
matplotlib.use('Qt5Agg')

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QStackedWidget
from PySide6 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class IntroPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel('Bienvenue sur la page d\'accueil !', self)
        label.setStyleSheet('font-size: 20pt;')
        layout.addWidget(label)
        layout.setAlignment(QtCore.Qt.AlignCenter) 
        button = QPushButton('Passer à la page suivante', self)
        button.clicked.connect(parent.nextPage)
        layout.addWidget(button)
        self.setLayout(layout)


class SinusoidalPlot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Graphique Sinusoidal avec Slider')
        layout = QVBoxLayout()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.slider_ax = plt.axes([0.2, 0.02, 0.75, 0.02])
        self.slider = Slider(self.slider_ax, 'Fréquence', 1, 10, valinit=1, valstep=1)
        self.slider.on_changed(self.updatePlot)

        self.setLayout(layout)

    def updatePlot(self, val):
        frequency = self.slider.val
        t = np.linspace(0, 2 * np.pi, 1000)
        y = np.sin(2 * np.pi * frequency * t)

        self.ax.clear()
        self.ax.plot(t, y)
        self.ax.set_xlabel('Temps')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_title(f'Graphique Sinusoidal (Fréquence : {frequency} Hz)')
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Application avec Pages')
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        intro_page = IntroPage(self)
        self.stacked_widget.addWidget(intro_page)

        sinusoidal_page = SinusoidalPlot(self)
        self.stacked_widget.addWidget(sinusoidal_page)

        self.current_page_index = 0

    def nextPage(self):
        self.current_page_index += 1
        if self.current_page_index >= self.stacked_widget.count():
            self.current_page_index = 0
        self.stacked_widget.setCurrentIndex(self.current_page_index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
