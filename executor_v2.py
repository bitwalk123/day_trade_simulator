import os
import sys

from PySide6.QtCore import QThreadPool, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes
from threads.broker import BrokerThreadLoop
from ui.dock_executor import DockExecutor
from ui.win_executor import WinExecutor
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
        self.broker = None

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
        self.win_main = win_main = WinExecutor(res)
        win_main.startClicked.connect(self.on_start_simulation)
        self.setCentralWidget(win_main)

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

    def on_start_simulation(self):
        print('start simulation!')
        self.broker = broker = BrokerThreadLoop(
            self.dock, self.win_main, self.threadpool
        )
        broker.errorMessage.connect(self.show_error_message)
        broker.threadFinished.connect(self.thread_complete)

        # シミュレーション開始
        broker.start()

    def show_error_message(self, msg):
        print(msg)

    def thread_complete(self, result: bool):
        if result:
            print('スレッド処理を正常終了しました。')
        else:
            print('スレッド処理を異常終了しました。')


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
