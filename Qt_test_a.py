import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PySide6 import QtCore

class WelcomePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        welcome_label = QLabel("Bienvenue sur la Page d'Accueil", self)
        welcome_label.setStyleSheet('font-size: 18pt; font-weight: bold;')

        

        start_button = QPushButton("Démarrer", self)
        start_button.setFixedSize(400, 50)
        start_button.clicked.connect(self.on_start_button_click)

        layout.addWidget(welcome_label, alignment=QtCore.Qt.AlignCenter)
        # Ajout d'un espace vertical de 20 pixels
        layout.addSpacing(20)

        layout.addWidget(start_button, alignment=QtCore.Qt.AlignCenter)

        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(layout)

    def on_start_button_click(self):
        # Ajoutez ici le code pour basculer vers la deuxième page
        self.parent().setCurrentIndex(1)  # 1 correspond à l'index de la deuxième page


class MenuPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        menu_label = QLabel("Menu", self)
        menu_label.setAlignment(QtCore.Qt.AlignCenter)
        menu_label.setStyleSheet('font-size: 18pt; font-weight: bold;')


        

        back_button = QPushButton("Accueil", self)
        back_button.setFixedSize(300, 60)
        back_button.clicked.connect(self.on_back_button_click)



        Pb_ivre_button = QPushButton("Pb initial", self)
        Pb_ivre_button.setFixedSize(300, 60)
        Pb_ivre_button.clicked.connect(self.go_to_probleme_init_page)

        Pollen_button = QPushButton("Pb pollen", self)
        Pollen_button.setFixedSize(300, 60)
        Pollen_button.clicked.connect(self.on_back_button_click)

        Diffusion_button = QPushButton("Pb diffusion", self)
        Diffusion_button.setFixedSize(300, 60)
        Diffusion_button.clicked.connect(self.on_back_button_click)

        Finance_button = QPushButton("Pb finance", self)
        Finance_button.setFixedSize(300, 60)
        Finance_button.clicked.connect(self.on_back_button_click)


        layout.addWidget(menu_label)
        # Ajout d'un espace vertical de 20 pixels
        layout.addSpacing(20)
        layout.addWidget(back_button)

        layout.addSpacing(20)
        layout.addWidget(Pb_ivre_button)

        layout.addSpacing(20)
        layout.addWidget(Pollen_button)

        layout.addSpacing(20)
        layout.addWidget(Diffusion_button)

        layout.addSpacing(20)
        layout.addWidget(Finance_button)

        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(layout)

    def on_back_button_click(self):
        # Ajoutez ici le code pour basculer vers la première page
        self.parent().setCurrentIndex(0)  # 0 correspond à l'index de la première page

    def go_to_probleme_init_page(self):
        self.parent().setCurrentIndex(2)

class PBInitialMainPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        welcome_label = QLabel("Bienvenue sur le Probleme Initial", self)
        welcome_label.setStyleSheet('font-size: 18pt; font-weight: bold;')

        

        start_button = QPushButton("Tracer", self)
        start_button.setFixedSize(400, 50)
        start_button.clicked.connect(self.on_start_button_click)

        layout.addWidget(welcome_label, alignment=QtCore.Qt.AlignCenter)
        # Ajout d'un espace vertical de 20 pixels
        layout.addSpacing(20)

        layout.addWidget(start_button, alignment=QtCore.Qt.AlignCenter)

        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(layout)

    def on_start_button_click(self):
        # Ajoutez ici le code pour basculer vers la deuxième page
        self.parent().setCurrentIndex(1)  # 1 correspond à l'index de la deuxième page


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Brownies')
        self.setFixedSize(800, 600)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        welcome_page = WelcomePage(self.stacked_widget)
        menu_page = MenuPage(self.stacked_widget)
        Pb_initial_page = PBInitialMainPage(self.stacked_widget)

        self.stacked_widget.addWidget(welcome_page)
        self.stacked_widget.addWidget(menu_page)
        self.stacked_widget.addWidget(Pb_initial_page)

        self.stacked_widget.setCurrentIndex(0)  # Afficher la première page par défaut

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
