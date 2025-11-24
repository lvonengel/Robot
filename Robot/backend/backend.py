import functools
from Robot.backend.HandDetectorCV import HandDetectorCV
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
import serial

class Backend(QObject):

    motors_connected = Signal(bool)


    def __init__(self):
        super().__init__()

        self.ser:serial.Serial | None = None
        self.motors = None
        self.hand_detector:HandDetectorCV|None = None


    def connect_signals(self):
        pass
        
    
    @staticmethod
    def serial_decorator(func):
        """
        Decorator for backend functions, to pop up a messagebox if the backend is not initialized.
        This should be called on any function that requires a backend to be connected to work
        """

        @functools.wraps(func)
        def backend_checker(*args, **kwargs):
            self, *_ = args
            if self.backend.ser is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("Serial is not Connected")
                msg.setInformativeText(
                    "Make sure the serial is connected before doing this"
                )
                msg.setWindowTitle("Serial Not Connected")
                msg.exec()
            else:
                return func(*args, **kwargs)

        return backend_checker


    def connect_serial(self):
        if self.motors is None:
            print("Connecting to Serial")
            #actually connect motors here
            try:
                self.ser = serial.Serial(port="COM3", baudrate=9600, timeout=1)
                self.motors_connected.emit(True)
            except:
                print("Could not connect to serial port")
                self.motors_connected.emit(False)


    def disconnect_serial(self):
        if self.motors is not None:
            print("Disconnecting Serial")
            #do some disconnecting
            self.motors_connected.emit(False)


    def start_live(self, frame_callback, error_callback=None):
        """
        Starts live for hand detection using CV
        """
        if self.hand_detector is None:
            self.hand_detector = HandDetectorCV(self)
        self.hand_detector.start_live(frame_callback, error_callback)
    

    def end_live(self):
        """
        Stops live for hand detection using CV
        """
        self.hand_detector.end_live()
        self.hand_detector = None