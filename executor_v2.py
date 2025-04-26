import os
import sys

from PySide6.QtCore import QThreadPool, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes
from ui.dock_executor import DockExecutor
from ui.panel_executor import PanelExecutor
from ui.toolbar_executor import ToolbarExecutor
from widgets.progress import ProgressBar
from widgets.statusbar import StatusBar


class Executor(QMainWindow):
    __app_name__ = 'Executor'
    __version__ = '2.0.0'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()

        # ウィンドウ・アイコンとタイトル
        self.setWindowIcon(QIcon(os.path.join(res.dir_image, 'start.png')))
        self.setWindowTitle('%s - %s' % (self.__app_name__, self.__version__))

        # =====================================================================
        #  UI
        # =====================================================================
        # ツールバー
        toolbar = ToolbarExecutor(res)
        toolbar.dirSelected.connect(self.exel_dir_selected)
        self.addToolBar(toolbar)

        # ドック
        self.dock = dock = DockExecutor(res)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # メイン・ウィンドウ
        panel = PanelExecutor(res)
        self.setCentralWidget(panel)

        # ステータスバー
        statusbar = StatusBar()
        self.setStatusBar(statusbar)

        self.pbar = pbar = ProgressBar()
        self.pbar.setRange(0, 100)
        statusbar.addPermanentWidget(pbar, stretch=1)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        event.accept()  # let the window close

    def exel_dir_selected(self, dir: str):
        self.dock.setExcelDir(dir)


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
