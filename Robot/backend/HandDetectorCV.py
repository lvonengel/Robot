import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtGui import QImage, QPixmap


class HandDetectorWorker(QObject):
    """
    Worker that runs the heavy processing for HandDetector class
    """
    # Sends frames to the GUI
    frame_ready = Signal(object)
    finished = Signal()
    error = Signal(str)
    
    def __init__(self, serial:serial.Serial, port="COM3", baudrate=9600):
        super().__init__()
        self.ser = serial
        self.port = port
        self.baudrate = baudrate
        self.running = False
        self.cap = None
    
    
    def run(self):
        """
        Runs the main hand detection processing.
        """
        try:
            self.cap = cv2.VideoCapture(0)
            detector = HandDetector(detectionCon=0.8, maxHands=1)
            
            hand_states = [["Wrist", False],
                          ["Index", False],
                          ["Middle", False],
                          ["Ring", False],
                          ["Thumb", False],
                          ["Pinky", False]]
            
            prev_time = 0
            self.running = True
            
            while self.running:
                success, frame = self.cap.read()
                if not success:
                    break
                
                hands, frame = detector.findHands(frame, draw=True)
                
                if hands:
                    hand = hands[0]
                    lmList = hand["lmList"]
                    
                    if len(lmList) >= 21:
                        j = 1
                        change = False
                        
                        for i in range(1, 6):
                            if i == 1:
                                if lmList[4][0] < lmList[3][0] and not hand_states[4][1]:
                                    hand_states[4][1] = True
                                    change = True
                                elif lmList[4][0] > lmList[3][0] and hand_states[4][1]:
                                    hand_states[4][1] = False
                                    change = True
                            else:
                                tip_id = i * 4
                                lower_joint_id = tip_id - 2
                                if lmList[tip_id][1] > lmList[lower_joint_id][1] and not hand_states[j][1]:
                                    hand_states[j][1] = True
                                    change = True
                                elif lmList[tip_id][1] < lmList[lower_joint_id][1] and hand_states[j][1]:
                                    hand_states[j][1] = False
                                    change = True
                                
                                if j == 3:
                                    j += 2
                                else:
                                    j += 1
                        
                        if change:
                            msg = ""
                            for i in range(6):
                                msg += "1" if hand_states[i][1] else "0"
                            msg += "\n"
                            if self.ser is not None:
                                self.ser.write(msg.encode("ascii"))
                            else:
                                print("Serial not connected, skipping write:", msg.strip())
                
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if prev_time else 0
                prev_time = curr_time
                
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)
                
                pixmap = self.convert_cv_to_pixmap(frame)
                self.frame_ready.emit(pixmap)
                
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.cleanup()
            self.finished.emit()
    

    def convert_cv_to_pixmap(self, cv_img):
        """
        Converts CV into a pixmap so that it can be displays in the GUI app.
        """
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_image)
    

    def stop(self):
        self.running = False
    

    def cleanup(self):
        if self.cap:
            self.cap.release()
        if self.ser:
            self.ser.close()


class HandDetectorCV:
    """
    Manages the thread and worker class
    """
    def __init__(self, backend):
        self.backend = backend
        self.thread = None
        self.worker = None
    

    def start_live(self, frame_callback, error_callback=None):
        """
        Start the hand tracking in a separate thread
        """

        # Stops if it's already live
        if self.thread is not None and self.thread.isRunning():
            return
        
        self.thread = QThread()
        self.worker = HandDetectorWorker(self.backend.ser)
        self.worker.moveToThread(self.thread)
        
        # start worker when thread starts
        self.thread.started.connect(self.worker.run)
        self.worker.frame_ready.connect(frame_callback)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        if error_callback:
            self.worker.error.connect(error_callback)
        
        self.thread.start()
    

    def end_live(self):
        """
        Stop the hand tracking adn stops the worker/thread
        """
        if self.worker:
            self.worker.stop() 
        if self.thread:
            self.thread.quit()
            self.thread.wait()