
from PySide6.QtCore import QObject, Signal, Slot, Property as QProperty, QTimer

class MotorsQObject(QObject):

    def __init__(self):
        super().__init__()

        self.homed = False

    def get_position(self):
        pass
    
    def get_speed(self):
        pass

    def reset_motor_speeds(self):
        pass

    def home_motors(self):
        pass
        

    homed_changed = Signal(bool)
    def get_homed(self) -> bool:
        return self.homed
    def set_homed(self, value: bool):
        if value != self.homed:
            self.homed = value
            self.homed_changed.emit(value)
    homed = QProperty(bool, get_homed, set_homed, notify=homed_changed)