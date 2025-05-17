import os
import sys

from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from structs.res import AppRes


class TradeSimulator(QMainWindow):
    __app_name__ = 'Trade Simulator'
    __version__ = '2.0.0'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()

        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)
        self.setFixedSize(1500, 900)


def main():
    app = QApplication(sys.argv)
    win = TradeSimulator()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
