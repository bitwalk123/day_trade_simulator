import pandas as pd
from PySide6.QtWidgets import (
    QHeaderView,
    QTableView,
)

from ui.model_dataframe import PandasModel


class WinOrderHistory(QTableView):

    def __init__(self, df: pd.DataFrame, formats: list):
        super().__init__()
        self.df = df
        self.formats = formats
        self.setWindowTitle('注文履歴')
        self.resize(600, 800)

        self.setStyleSheet("""
            QTableView {
                font-family: monospace;
            }
        """)

        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        # self.setSelectionBehavior(QTableView.SelectRows)

        model = PandasModel(df, formats)
        self.setModel(model)

        header = self.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
