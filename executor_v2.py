import os
import sys

from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes
from ui.toolbar_executor import ToolbarExecutor


class Executor(QMainWindow):
    __app_name__ = 'Executor'
    __version__ = '2.0.0'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()

        # ウィンドウ・アイコンとタイトル
        icon = QIcon(os.path.join(res.dir_image, 'start.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)

        # =====================================================================
        #  UI
        # =====================================================================
        # ツールバー
        toolbar = ToolbarExecutor(res)
        self.addToolBar(toolbar)


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
