import numpy as np
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from structs.pair import PairXY
from structs.res import AppRes
from widgets.charts import ChartOverlay, ChartNavigation


class WinOverlayAnalysis(QMainWindow):
    def __init__(self, dict_target: dict, res: AppRes):
        super().__init__()
        self.dict_target = dict_target
        self.res = res
        self.list_obj = list()

        self.setWindowTitle('重ね合わせ')

        self.canvas = canvas = ChartOverlay(self.res)
        self.setCentralWidget(canvas)

        self.navtoolbar = navtoolbar = ChartNavigation(canvas)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

        df_ohlc_1m = dict_target['1m']
        obj: PairXY | None = None
        x_max = 0
        for x, y in zip(df_ohlc_1m['Period'], df_ohlc_1m['Diff']):
            if np.isnan(x):
                continue
            if x == 0:
                y = 0
                if obj is not None:
                    if obj.length() > 1:
                        self.list_obj.append(obj)
                        if x_max < obj.length():
                            x_max = obj.length()
                obj = PairXY(x, y)
            else:
                obj.appendXY(x, y)

        self.canvas.setXMax(x_max)

        self.on_plot_all()

    def on_plot_all(self):
        self.canvas.plot(self.list_obj)
