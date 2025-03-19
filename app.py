import os
import sys

from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QProgressBar,
    QTabWidget,
)

from structs.res import AppRes
from threads.preprocs import WorkerPrepDataset
from ui.toolbar import ToolBar
from ui.win_main import WinMain
from widgets.statusbar import StatusBar
from widgets.tabwidget import TabWidget


class TradeSimulator(QMainWindow):
    __app_name__ = 'Trade Simulator'

    def __init__(self):
        super().__init__()
        self.res = res=AppRes()
        self.threadpool = QThreadPool()

        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)
        self.setFixedSize(1500, 900)

        # ツールバー
        toolbar = ToolBar(self.res)
        toolbar.fileSelected.connect(self.on_file_selected)
        self.addToolBar(toolbar)

        self.base = base = TabWidget()
        base.setTabPosition(QTabWidget.TabPosition.South)
        self.setCentralWidget(base)

        statusbar = StatusBar()
        self.setStatusBar(statusbar)

        self.pbar = pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        statusbar.addPermanentWidget(pbar, stretch=1)

    def on_file_selected(self, file_excel: str):
        """
        選択した Excel ファイルの読み込みと解析用データ準備
        :param file_excel:
        :return:
        """
        prep_ds = WorkerPrepDataset(file_excel)
        prep_ds.updateProgress.connect(self.on_status_update)
        prep_ds.threadFinished.connect(self.on_dataset_ready)
        self.threadpool.start(prep_ds)

    def on_dataset_ready(self, list_target):
        """
        データセットに基づき、銘柄毎のタブ画面を作成
        :param list_target:
        :return:
        """
        # 現在のタブをすべて削除
        self.base.deleteAllTabs()
        # 新しいタブを追加
        for dict_target in list_target:
            code = dict_target['code']
            tabobj = WinMain(self.res, dict_target, self.threadpool, self.pbar)
            self.base.addTab(tabobj, code)
        # 進捗をリセット
        self.pbar.reset()


    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)


def main():
    app = QApplication(sys.argv)
    win = TradeSimulator()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
