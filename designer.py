import sys

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QMainWindow, QApplication

from structs.res import AppRes


class Designer(QMainWindow):
    __app_name__ = 'Experiment Designer'

    def __init__(self):
        super().__init__()
        self.res = res=AppRes()
        self.threadpool = QThreadPool()

def main():
    app = QApplication(sys.argv)
    win = Designer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
