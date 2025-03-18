import sys

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget, QStatusBar, QProgressBar,
)

from funcs.preprocs import prep_dataset
from structs.res import AppRes
from threads.preprocs import WorkerPrepDataset
from ui.toolbar import ToolBar
from ui.win_main import WinMain


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

        self.base = base = QTabWidget()
        base.setTabPosition(QTabWidget.TabPosition.South)
        self.setCentralWidget(base)

        statusbar = QStatusBar()
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
        prep_datasheet = WorkerPrepDataset(file_excel)
        prep_datasheet.updateProgress.connect(self.on_status_update)
        prep_datasheet.threadFinished.connect(self.on_dataset_ready)
        self.threadpool.start(prep_datasheet)

    def on_dataset_ready(self, list_target):
        """
        データセットに基づき、銘柄毎のタブ画面を作成
        :param list_target:
        :return:
        """
        for dict_target in list_target:
            code = dict_target['code']
            self.base.addTab(WinMain(self.res, dict_target), code)
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
