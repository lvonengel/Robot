
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QWidget, QTabWidget, QGridLayout, QLabel, QPushButton, QLineEdit

from Robot.backend.backend import Backend
from Robot.frontend.parts.HandCV import HandCV
from Robot.frontend.parts.hand import Hand


class MainWindow(QWidget):
    '''
    Overall main window where everything is
    '''

    def __init__(self, backend:Backend):
        super().__init__()
        self.backend = backend

        self.create_widgets()
        self.connect_signals()


    def create_widgets(self):
        layout = QGridLayout()

        self.connect_motors_button = QPushButton("Connect Motors")
        self.connect_motors_status = QLineEdit("NOT CONNECTED")
        self.connect_motors_status.setStyleSheet("background:red;")
        self.connect_motors_status.setEnabled(False)
        
        self.parts_tab = QTabWidget()

        self.hand = Hand(self.backend)
        self.handCV = HandCV(self.backend)

        self.parts_tab.addTab(self.hand, "Hand")
        self.parts_tab.addTab(self.handCV, "Hand CV")

        layout.addWidget(self.connect_motors_button, 0, 0)
        layout.addWidget(self.connect_motors_status, 0, 1)
        layout.addWidget(self.parts_tab, 1, 0, 1, 2)

        self.setLayout(layout)


    def connect_signals(self):
        self.connect_motors_button.clicked.connect(self.backend.connect_serial)
        self.backend.motors_connected.connect(self.set_background)


    def set_background(self, connected:bool):
        if connected:
            self.connect_motors_status.setStyleSheet("background:green;")
            self.connect_motors_status.setText("CONNECTED")
        else:
            self.connect_motors_status.setStyleSheet("background:red;")
    