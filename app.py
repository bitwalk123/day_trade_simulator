#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from sim.simulator import WorkerSimulator
from structs.res import AppRes
from ui.dock import DockSimulator
from ui.toolbar import ToolBar
from widgets.charts import Canvas, ChartNavigation


class Analyzer(QMainWindow):
    __app_name__ = 'PSAR Simulator'

    def __init__(self):
        super().__init__()
        self.res = AppRes()
        self.threadpool = QThreadPool()

        self.setWindowTitle(self.__app_name__)
        self.setFixedSize(1200, 800)

        toolbar = ToolBar(self.res)
        toolbar.readDataFrame.connect(self.on_read_df)
        self.addToolBar(toolbar)

        self.dock = dock = DockSimulator()
        dock.simStarted.connect(self.on_start)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        self.canvas = canvas = Canvas(self.res)
        self.setCentralWidget(canvas)

        self.navtoolbar = navtoolbar = ChartNavigation(canvas)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

    def on_end(self):
        """
        スレッド処理の終了
        :return:
        """
        self.dock.updateStatus('停止')

    def on_read_df(self, dict_target: dict):
        self.canvas.plot(dict_target)
        self.dock.setInit(dict_target)

    def on_start(self, dict_target: dict):
        """
        シミュレーターを別スレッドで起動
        :param dict_target:
        :return:
        """
        worker = WorkerSimulator(dict_target)
        # 進捗ウィジェットの開始・終了レンジを設定
        self.dock.setProgressRange(*worker.getTimeRange())
        # シグナルの処理
        worker.threadFinished.connect(self.on_end)
        worker.updateProfit.connect(self.on_update_profit)
        worker.updateProgress.connect(self.on_update_progress)
        worker.updateSystemTime.connect(self.on_update_system_time)
        worker.updateTickPrice.connect(self.on_update_tick_price)
        worker.updateTrend.connect(self.on_update_trend)
        # ステータス表示の変更
        self.dock.updateStatus('稼働中')
        # スレッドで処理を開始
        self.threadpool.start(worker)

    def on_update_profit(self, dict_update: dict):
        """
        含み益の更新
        :param dict_update:
        :return:
        """
        self.dock.updateProfit(dict_update)

    def on_update_progress(self, tick: int):
        """
        進捗ウィジェットの更新
        :param tick:
        :return:
        """
        self.dock.setProgressValue(tick)

    def on_update_system_time(self, time_str: str):
        """
        システム時刻の更新
        :param time_str:
        :return:
        """
        self.dock.updateSystemTime(time_str)

    def on_update_tick_price(self, time_str: str, price: float):
        """
        ティックデータの更新
        :param time_str:
        :param price:
        :return:
        """
        self.dock.updateTickPrice(time_str, price)

    def on_update_trend(self, trend: int):
        self.dock.updateTrend(trend)


def main():
    app = QApplication(sys.argv)
    win = Analyzer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
