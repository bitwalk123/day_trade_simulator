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
    __version__ = '2.1.0'

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
        if self.broker is not None:
            self.broker.deleteLater()
        event.accept()  # let the window close

    def exel_dir_selected(self, dir: str):
        self.dock.setExcelDir(dir)

    def get_params4broker(self) -> dict:
        """
        BrokerThreadLoop インスタンスへ渡すパラメータ
        """
        params = dict()
        params['res'] = self.res
        params['threadpool'] = self.threadpool
        params['dock'] = self.dock
        params['panel'] = self.win_main
        params['pbar'] = self.pbar

        return params

    def on_start_simulation(self):
        """
        シミュレーション起動
        """
        params = self.get_params4broker()
        self.broker = broker = BrokerThreadLoop(params)
        broker.errorMessage.connect(self.on_show_error_message)
        broker.simulationFinished.connect(self.on_simulation_finished)

        # BrokerThreadLoop インスタンスでシミュレーション開始
        print('start simulation!')
        broker.start()

    def on_show_error_message(self, msg):
        print(msg)

    def on_simulation_finished(self, result: bool):
        if result:
            print('シミュレーションを正常終了しました。')
        else:
            print('シミュレーションを異常終了しました。')


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
