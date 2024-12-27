#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

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
        print(df)


def main():
    app = QApplication(sys.argv)
    win = Analyzer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
