#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from structs.res import AppRes
from tech.psar import (
    calc_PSAR,
    calc_PSAR0,
    initialize,
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

    def on_read_df(self, df: pd.DataFrame):
        """
        Yahoo Finance から取得した１分足データ
        :param df:
        :return:
        """
        # PSAR の算出
        df = initialize(df)
        for i in range(len(df)):
            if i == 1:
                calc_PSAR0(df, i)
            elif i > 1:
                calc_PSAR(df, i)
        df['bull'] = df[df['Trend'] == 1]['PSAR']
        df['bear'] = df[df['Trend'] == -1]['PSAR']

        self.canvas.plot(df)


def main():
    app = QApplication(sys.argv)
    win = Analyzer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
