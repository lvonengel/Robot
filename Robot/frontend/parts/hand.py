from PySide6.QtWidgets import QWidget, QLabel, QDoubleSpinBox, QGridLayout, QPushButton
from PySide6.QtCore import Slot, Qt

from Robot.backend.enums import Part


class Hand(QWidget):

    def __init__(self, backend):
        super().__init__()
        self.backend = backend

        self.create_widgets()
        self.connect_signals()


    def create_widgets(self):
        layout = QGridLayout()

        self.finger_label = QLabel("Finger")
        self.quick_action_label = QLabel("Quick Action")

        self.thumb_label = QLabel("Thumb")
        self.thumb_pos = QDoubleSpinBox()
        self.thumb_pos.setRange(0, 180)
        self.thumb_pos.setMinimumWidth(150)

        self.thumb_rest = QPushButton("Rest")
        self.thumb_mid = QPushButton("Middle")
        self.thumb_max = QPushButton("Max")

        self.index_label = QLabel("Index")
        self.index_pos = QDoubleSpinBox()
        self.index_pos.setRange(0, 180)
        self.index_pos.setMinimumWidth(150)

        self.index_rest = QPushButton("Rest")
        self.index_mid = QPushButton("Middle")
        self.index_max = QPushButton("Max")

        self.middle_label = QLabel("Middle")
        self.middle_pos = QDoubleSpinBox()
        self.middle_pos.setRange(0, 180)
        self.middle_pos.setMinimumWidth(150)

        self.middle_rest = QPushButton("Rest")
        self.middle_mid = QPushButton("Middle")
        self.middle_max = QPushButton("Max")

        self.ring_label = QLabel("Ring")
        self.ring_pos = QDoubleSpinBox()
        self.ring_pos.setRange(0, 180)
        self.ring_pos.setMinimumWidth(150)

        self.ring_rest = QPushButton("Rest")
        self.ring_mid = QPushButton("Middle")
        self.ring_max = QPushButton("Max")

        self.pinky_label = QLabel("Pinky")
        self.pinky_pos = QDoubleSpinBox()
        self.pinky_pos.setRange(0, 180)
        self.pinky_pos.setMinimumWidth(150)

        self.pinky_rest = QPushButton("Rest")
        self.pinky_mid = QPushButton("Middle")
        self.pinky_max = QPushButton("Max")

        layout.addWidget(self.finger_label, 0, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.quick_action_label, 0, 2, alignment=Qt.AlignRight)

        thumb_index = 1
        layout.addWidget(self.thumb_label, thumb_index, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.thumb_pos, thumb_index, 1, alignment=Qt.AlignLeft)
        layout.addWidget(self.thumb_rest, thumb_index, 2, alignment=Qt.AlignLeft)
        layout.addWidget(self.thumb_mid, thumb_index, 3, alignment=Qt.AlignLeft)
        layout.addWidget(self.thumb_max, thumb_index, 4, alignment=Qt.AlignLeft)

        index_index = 2
        layout.addWidget(self.index_label, index_index, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.index_pos, index_index, 1, alignment=Qt.AlignLeft)
        layout.addWidget(self.index_rest, index_index, 2, alignment=Qt.AlignLeft)
        layout.addWidget(self.index_mid, index_index, 3, alignment=Qt.AlignLeft)
        layout.addWidget(self.index_max, index_index, 4, alignment=Qt.AlignLeft)

        middle_index = 3
        layout.addWidget(self.middle_label, middle_index, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.middle_pos, middle_index, 1, alignment=Qt.AlignLeft)
        layout.addWidget(self.middle_rest, middle_index, 2, alignment=Qt.AlignLeft)
        layout.addWidget(self.middle_mid, middle_index, 3, alignment=Qt.AlignLeft)
        layout.addWidget(self.middle_max, middle_index, 4, alignment=Qt.AlignLeft)

        ring_index = 4
        layout.addWidget(self.ring_label, ring_index, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.ring_pos, ring_index, 1, alignment=Qt.AlignLeft)
        layout.addWidget(self.ring_rest, ring_index, 2, alignment=Qt.AlignLeft)
        layout.addWidget(self.ring_mid, ring_index, 3, alignment=Qt.AlignLeft)
        layout.addWidget(self.ring_max, ring_index, 4, alignment=Qt.AlignLeft)

        pinky_index = 5
        layout.addWidget(self.pinky_label, pinky_index, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.pinky_pos, pinky_index, 1, alignment=Qt.AlignLeft)
        layout.addWidget(self.pinky_rest, pinky_index, 2, alignment=Qt.AlignLeft)
        layout.addWidget(self.pinky_mid, pinky_index, 3, alignment=Qt.AlignLeft)
        layout.addWidget(self.pinky_max, pinky_index, 4, alignment=Qt.AlignLeft)
    

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        self.setLayout(layout)


    def connect_signals(self):
        self.index_pos.valueChanged.connect(lambda: self.set_motor_position(Part.INDEX, self.index_pos.value()))



    def set_motor_position(self, part:Part, position:float):
        print(f"Setting part: {part.value} to position: {position}")