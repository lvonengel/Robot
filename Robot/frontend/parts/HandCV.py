from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from Robot.backend.backend import Backend


class HandCV(QWidget):

    def __init__(self, backend:Backend):
        super().__init__()
        self.backend = backend
        self.is_live = False

        self.create_widgets()
        self.connect_signals()


    def create_widgets(self):
        layout = QVBoxLayout()

        self.live_image = QLabel()
        pixmap = QPixmap('Robot/resources/no_camera.png')
        scaled_pixmap = pixmap.scaled(600, 500, Qt.AspectRatioMode.KeepAspectRatio, 
                                     Qt.TransformationMode.SmoothTransformation)
        self.live_image.setPixmap(scaled_pixmap)
        self.live_image.setAlignment(Qt.AlignCenter)

        button_layout_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout_widget.setLayout(button_layout)

        self.start_live_btn = QPushButton("Start Live")
        self.end_live_btn = QPushButton("End Live")
        self.end_live_btn.setEnabled(False)
        
        button_layout.addWidget(self.start_live_btn)
        button_layout.addWidget(self.end_live_btn)

        layout.addWidget(self.live_image)
        layout.addWidget(button_layout_widget)

        self.setLayout(layout)


    def connect_signals(self):
        self.start_live_btn.clicked.connect(self.on_start_live)
        self.end_live_btn.clicked.connect(self.on_end_live)
    
    def on_start_live(self):
        """
        Start the live for the CV
        """
        self.backend.start_live(self.update_frame, self.handle_error)
        self.start_live_btn.setEnabled(False)
        self.end_live_btn.setEnabled(True)
        self.is_live = True
    
    def on_end_live(self):
        """
        Stop the live for the CV
        """
        self.backend.end_live()
        self.start_live_btn.setEnabled(True)
        self.end_live_btn.setEnabled(False)
        self.is_live = False
    

    def update_frame(self, pixmap):
        """
        Continously updates the frame
        """
        scaled_pixmap = pixmap.scaled(600, 500, Qt.AspectRatioMode.KeepAspectRatio, 
                                     Qt.TransformationMode.SmoothTransformation)
        self.live_image.setPixmap(scaled_pixmap)
    

    def handle_error(self, error_msg):
        """
        Prints out error and ends live
        """
        print(f"Error: {error_msg}")
        self.on_end_live()