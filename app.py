import sys

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from structs.res import AppRes
from ui.toolbar import ToolBar


class TradeSimulator(QMainWindow):
    __app_name__ = 'Trade Simulator'

    def __init__(self):
        super().__init__()
        self.res = AppRes()
        self.threadpool = QThreadPool()

        self.setWindowTitle(self.__app_name__)
        self.setFixedSize(1200, 800)

        toolbar = ToolBar(self.res)
        toolbar.fileSelected.connect(self.on_file_selected)
        self.addToolBar(toolbar)

    def on_file_selected(self, file_excel: str):
        print(file_excel)


def main():
    app = QApplication(sys.argv)
    win = TradeSimulator()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
