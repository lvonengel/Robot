from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Signal, Property as QProperty
from PySide6.QtGui import QPixmap

class HandCV(QWidget):

    def __init__(self, backend):
        super().__init__()
        self.backend = backend

        self.create_widgets()
        self.connect_signals()

    def create_widgets(self):
        layout = QVBoxLayout()

        live_image = QLabel()
        pixmap = QPixmap('Robot/resources/no_camera.png')
        live_image.setPixmap(pixmap)
        scaled_pixmap = pixmap.scaled(600, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        live_image.setPixmap(scaled_pixmap)

        button_layout_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout_widget.setLayout(button_layout)

        self.start_live_btn = QPushButton("Start Live")
        self.end_live_btn = QPushButton("End Live")
        button_layout.addWidget(self.start_live_btn)
        button_layout.addWidget(self.end_live_btn)

        layout.addWidget(live_image)
        layout.addWidget(button_layout_widget)

        self.setLayout(layout)

    def connect_signals(self):
        pass
        # self.start_live_btn.clicked.connect(self.backend.)
    
    
    is_live_changed = Signal(bool)
    def get_is_live(self) -> bool:
        return self.is_live
    def set_is_live(self, value: bool):
        if value != self.is_live:
            self.is_live = value
            self.is_live_changed.emit(value)
    is_live = QProperty(bool, get_is_live, set_is_live, notify=is_live_changed)