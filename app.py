import os
import sys
from PySide6.QtCore import QSize, QThread
from PySide6.QtWidgets import QApplication, QMainWindow


from Robot.backend.backend import Backend
from Robot.frontend.main_window import MainWindow


class App(QMainWindow):
    def __init__(self, root_folder: str):
        super().__init__()

        self.setWindowTitle("Robotic Control App")
        self.setMinimumSize(QSize(500, 500))

        self.backend = Backend()
        self.backend_thread = QThread()
        self.backend.moveToThread(self.backend_thread)
        self.backend_thread.start()

        
        self.mainWindow = MainWindow(self.backend)
        self.setCentralWidget(self.mainWindow)

        qss_path = os.path.join(root_folder, "Robot", "resources", "widget_styling.qss")
        if os.path.exists(qss_path):
            with open(qss_path, encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())
        else:
            raise FileNotFoundError("QSS Stylesheet not found")

    def closeApp(self):
        if self.backend_thread.isRunning():
            self.backend_thread.quit()


if __name__ == "__main__":
    root_folder = os.path.dirname(__file__)
    print("root folder", root_folder)

    app = QApplication(sys.argv)
    window = App(root_folder)
    window.show()
    app.exec()
