import pandas as pd
from PySide6.QtWidgets import (
    QHeaderView,
    QMainWindow,
    QTableView,
)

from ui.model_dataframe import PandasModel


class WinOrderHistory(QMainWindow):

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df
        self.setWindowTitle('注文履歴')
        self.resize(600, 800)

        view = QTableView()
        self.setCentralWidget(view)

        view.setAlternatingRowColors(True)
        # view.horizontalHeader().setStretchLastSection(True)
        # view.setSelectionBehavior(QTableView.SelectRows)

        model = PandasModel(df)
        view.setModel(model)

        header = view.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

