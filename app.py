#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from sim.simulator import Timer4Sim
from structs.res import AppRes
from ui.dock import DockSimulator
from ui.toolbar import ToolBar
from widgets.charts import Canvas, ChartNavigation


class Analyzer(QMainWindow):
    __app_name__ = 'PSAR Simulator'

    def __init__(self):
        super().__init__()
        self.res = AppRes()
        self.timer = timer = Timer4Sim()
        timer.updateSystemTime.connect(self.on_update_system_time)
        timer.updateTickPrice.connect(self.on_update_tick_price)

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

    def on_read_df(self, dict_target: dict):
        self.canvas.plot(dict_target)
        self.dock.setInit(dict_target)

    def on_start(self, dict_target: dict):
        self.timer.start(dict_target)

    def on_update_system_time(self, time_str: str):
        self.dock.updateSystemTime(time_str)

    def on_update_tick_price(self, time_str: str, price: float):
        self.dock.updateTickPrice(time_str, price)


def main():
    app = QApplication(sys.argv)
    win = Analyzer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
