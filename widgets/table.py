import pandas as pd
from PySide6.QtWidgets import QTableView, QHeaderView

from ui.model_dataframe import PandasModel


class TableView(QTableView):
    def __init__(self, df: pd.DataFrame, formats: list):
        super().__init__()
        self.setStyleSheet("""
            QTableView {
                font-family: monospace;
                background-color: white;
                color: black;
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
