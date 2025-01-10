#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from structs.res import AppRes
from tech.psar import (
    psarStepByStep,
)
from ui.toolbar import ToolBar
from widgets.charts import Canvas, ChartNavigation


class Analyzer(QMainWindow):
    __app_name__ = 'PSAR Simulator'

    def __init__(self):
        super().__init__()
        self.res = AppRes()
        self.setWindowTitle(self.__app_name__)
        self.setFixedSize(1800, 800)

        toolbar = ToolBar(self.res)
        toolbar.readDataFrame.connect(self.on_read_df)
        self.addToolBar(toolbar)

        self.canvas = canvas = Canvas(self.res)
        self.setCentralWidget(canvas)

        self.navtoolbar = navtoolbar = ChartNavigation(canvas)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

    def on_read_df(self, dict_df: dict):
        """
        Yahoo Finance から取得した１分足データ
        :param df:
        :return:
        """
        # １分足のOHLCデータ
        df_1m = dict_df['1m']
        # df = psarStepByStep(df_1m)
        # self.canvas.plot(df)


def main():
    app = QApplication(sys.argv)
    win = Analyzer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
