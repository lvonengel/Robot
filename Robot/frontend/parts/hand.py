from PySide6.QtWidgets import QWidget, QLabel, QDoubleSpinBox, QGridLayout, QPushButton
from PySide6.QtCore import Qt

from Robot.backend.backend import Backend
from Robot.backend.enums import Part


class Hand(QWidget):

    def __init__(self, backend: Backend):
        super().__init__()
        self.backend = backend
        
        # Store finger widgets in dictionaries for easy access
        self.finger_spinboxes = {}
        
        self.create_widgets()
        self.connect_signals()

    def create_widgets(self):
        layout = QGridLayout()
        
        # Headers
        layout.addWidget(QLabel("Finger"), 0, 0, alignment=Qt.AlignRight)
        layout.addWidget(QLabel("Quick Action"), 0, 2, alignment=Qt.AlignRight)
        
        # Define fingers with their Part enum
        fingers = [
            ("Thumb", Part.THUMB),
            ("Index", Part.INDEX),
            ("Middle", Part.MIDDLE),
            ("Ring", Part.RING),
            ("Pinky", Part.PINKY)
        ]
        
        # Create widgets for each finger
        for row, (name, part) in enumerate(fingers, start=1):
            # Label
            layout.addWidget(QLabel(name), row, 0, alignment=Qt.AlignRight)
            
            # SpinBox
            spinbox = QDoubleSpinBox()
            spinbox.setRange(0, 180)
            spinbox.setMinimumWidth(150)
            spinbox.valueChanged.connect(lambda val, p=part: self.set_motor_position(p, val))
            self.finger_spinboxes[part] = spinbox
            layout.addWidget(spinbox, row, 1, alignment=Qt.AlignLeft)
            
            # Quick action buttons
            rest_btn = QPushButton("Rest")
            rest_btn.clicked.connect(lambda _, p=part: self.set_motor_position(p, 0))
            layout.addWidget(rest_btn, row, 2, alignment=Qt.AlignLeft)
            
            mid_btn = QPushButton("Middle")
            mid_btn.clicked.connect(lambda _, p=part: self.set_motor_position(p, 90))
            layout.addWidget(mid_btn, row, 3, alignment=Qt.AlignLeft)
            
            max_btn = QPushButton("Max")
            max_btn.clicked.connect(lambda _, p=part: self.set_motor_position(p, 180))
            layout.addWidget(max_btn, row, 4, alignment=Qt.AlignLeft)
        
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        self.setLayout(layout)


    def connect_signals(self):
        pass 

    @Backend.serial_decorator
    def set_motor_position(self, part: Part, position: float):
        print(f"Setting part: {part.value} to position: {position}")
        
        # Check if serial is connected
        if self.backend.ser is None:
            print("Serial not connected!")
            return
            
        msg = f"{part.value}{position}\n"  # Added \n for Arduino
        self.backend.ser.write(msg.encode("ascii"))