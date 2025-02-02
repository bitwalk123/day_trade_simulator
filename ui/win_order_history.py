import pandas as pd
from PySide6.QtWidgets import (
    QHeaderView,
    QMainWindow,
    QTableView,
)

from ui.model_dataframe import PandasModel


class WinOrderHistory(QMainWindow):

    def __init__(self, df: pd.DataFrame, formats: list):
        super().__init__()
        self.df = df
        self.formats = formats
        self.setWindowTitle('注文履歴')
        self.resize(600, 800)

        view = QTableView()
        view.setStyleSheet("""
            QTableView {
                font-family: monospace;
            }
        """)
        self.setCentralWidget(view)

        view.setAlternatingRowColors(True)
        # view.horizontalHeader().setStretchLastSection(True)
        # view.setSelectionBehavior(QTableView.SelectRows)

        model = PandasModel(df, formats)
        view.setModel(model)

        header = view.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
