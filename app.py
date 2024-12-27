#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from tech.psar import initialize, calc_PSAR0, calc_PSAR
from ui.toolbar import ToolBar


class Analyzer(QMainWindow):
    __app_name__ = 'PSAR Simulator'

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.__app_name__)

        toolbar = ToolBar()
        toolbar.readDataFrame.connect(self.on_read_df)
        self.addToolBar(toolbar)

    def on_read_df(self, df: pd.DataFrame):
        """
        Yahoo Finance から取得した１分足データ
        :param df:
        :return:
        """
        df = initialize(df)
        for i in range(len(df)):
            if i == 1:
                calc_PSAR0(df, i)
            elif i > 1:
                calc_PSAR(df, i)
        print(df)


def main():
    app = QApplication(sys.argv)
    win = Analyzer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
