import os

import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QToolBar,
    QToolButton,
)

from structs.res import AppRes
from widgets.labels import (
    LabelTitle,
    LabelUnit,
    LabelValue, LabelFinance,
)
from widgets.table import TableView


class WinOrderHistory(QMainWindow):
    requestOrderHistoryHTML = Signal()

    def __init__(self, res: AppRes, df: pd.DataFrame, formats: list, total: float):
        super().__init__()
        self.res = res
        self.df = df
        self.formats = formats
        self.setWindowTitle('注文履歴')
        self.resize(600, 800)

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        but_html = QToolButton()
        but_html.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'html.png'))
        )
        but_html.setToolTip('売買履歴（HTML出力）')
        but_html.clicked.connect(self.on_order_history_html)
        toolbar.addWidget(but_html)

        tbl = TableView(df, formats)
        self.setCentralWidget(tbl)

        statusbar = QStatusBar()
        self.add_statusbar_widgets(statusbar, total)
        self.setStatusBar(statusbar)

    def add_statusbar_widgets(self, statusbar: QStatusBar, total: float):
        labTotal = LabelTitle('合計損益')
        labTotal.setFixedWidth(200)
        statusbar.addWidget(labTotal)

        objTotal = LabelFinance(total)
        statusbar.addWidget(objTotal)

        unitTotal = LabelUnit('円')
        statusbar.addWidget(unitTotal, stretch=1)

    def on_order_history_html(self):
        self.requestOrderHistoryHTML.emit()
