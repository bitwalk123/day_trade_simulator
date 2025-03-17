#!/usr/bin/env python
# coding: utf-8
import os
import sys

import pandas as pd
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from funcs.conv import df_to_html
from sim.simulator import WorkerSimulator
from structs.app_enum import SimulationMode
from structs.res import AppRes
from ui.dock import DockSimulator
from ui.toolbar import ToolBar
from ui.win_order_history import WinOrderHistory
from ui.win_overlay import WinOverlayAnalysis
from widgets.charts import Canvas, ChartNavigation


class TradeSimulator(QMainWindow):
    __app_name__ = 'Trade Simulator'

    def __init__(self):
        super().__init__()
        self.res = AppRes()
        self.threadpool = QThreadPool()

        # 注文履歴
        self.order_hist: WinOrderHistory | None = None  # 注文履歴
        self.df_order: pd.DataFrame | None = None
        self.column_format: list | None = None

        # 重ね合わせ解析
        self.overlay: WinOverlayAnalysis | None = None

        self.setWindowTitle(self.__app_name__)
        self.setFixedSize(1200, 800)

        toolbar = ToolBar(self.res)
        toolbar.readyDataset.connect(self.on_show_target)
        self.addToolBar(toolbar)

        self.dock = dock = DockSimulator(self.res)
        dock.requestAutoSimStart.connect(self.on_start_autosim)
        dock.requestOrderHistory.connect(self.on_order_history)
        dock.requestOrderHistoryHTML.connect(self.on_order_history_html)
        dock.requestSimulationStart.connect(self.on_start_sim)
        dock.requestOverlayAnalysis.connect(self.on_overlay_anaysis)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        self.canvas = canvas = Canvas(self.res)
        self.setCentralWidget(canvas)

        self.navtoolbar = navtoolbar = ChartNavigation(canvas)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

    def on_end(self, df: pd.DataFrame, column_format: list, mode: SimulationMode, result: dict):
        """
        スレッド処理の終了
        :param df:
        :param column_format:
        :return:
        """
        self.dock.updateStatus('停止')
        self.df_order = df
        self.column_format = column_format

        if mode == SimulationMode.EXPLORE:
            self.on_end_autosim(result)

    def on_end_autosim(self, result: dict):
        self.dock.setAutoSimResult(result)

    def on_order_history(self):
        if self.df_order is None:
            return

        if self.order_hist is not None:
            self.order_hist.hide()
            self.order_hist.deleteLater()
        self.order_hist = WinOrderHistory(self.df_order, self.column_format)
        self.order_hist.show()

    def on_order_history_html(self):
        if self.df_order is None:
            return
        list_html = df_to_html(self.df_order, self.column_format)

        home = os.path.expanduser("~")
        name_html = os.path.join(home, 'result.html')
        with open(name_html, mode='w') as f:
            f.writelines(list_html)

    def on_overlay_anaysis(self, dict_target: dict):
        if self.overlay is not None:
            self.overlay.hide()
            self.overlay.deleteLater()
        self.overlay = WinOverlayAnalysis(dict_target, self.res)
        self.overlay.show()

    def on_show_target(self, dict_target: dict):
        self.canvas.plot(dict_target)
        self.dock.setInit(dict_target)

    def on_start_sim(self, dict_target: dict, params: dict, mode=SimulationMode.NORMAL):
        """
        シミュレーターを別スレッドで起動
        :param dict_target:
        :return:
        """
        worker = WorkerSimulator(dict_target, params, mode)
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

    def on_start_autosim(self, dict_target: dict, params: dict):
        self.on_show_target(dict_target)

        mode = SimulationMode.EXPLORE
        self.on_start_sim(dict_target, params, mode)

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
    win = TradeSimulator()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
