import numpy as np
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from structs.pair import PairXY
from structs.res import AppRes
from ui.toolbar_overlay import ToolbarOverlayAnalysis
from widgets.charts import ChartOverlay, ChartNavigation


class WinOverlayAnalysis(QMainWindow):
    def __init__(self, dict_target: dict, res: AppRes):
        super().__init__()
        self.dict_target = dict_target
        self.res = res
        self.list_obj = list()
        self.counter_obj = 0

        self.setWindowTitle('重ね合わせ')

        self.toolbar = toolbar = ToolbarOverlayAnalysis(self.res)
        toolbar.backClicked.connect(self.on_back)
        toolbar.playClicked.connect(self.on_play)
        self.addToolBar(toolbar)

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
        y_min = 0
        y_max = 0
        for t, x, y in zip(df_ohlc_1m.index, df_ohlc_1m['Period'], df_ohlc_1m['Diff']):
            if np.isnan(x):
                continue
            if x == 0:
                y = 0
                if obj is not None:
                    if obj.length() > 1:
                        self.list_obj.append(obj)
                        if x_max < obj.length():
                            x_max = obj.length()
                obj = PairXY(t, x, y)
            else:
                obj.appendXY(x, y)
            if y < y_min:
                y_min = y
            if y_max < y:
                y_max = y
        # X軸の最大値
        self.canvas.setAxisRange(x_max, y_min, y_max)

        # とりあえず全てをプロット
        self.on_plot_all()

    def on_plot_all(self):
        self.canvas.plot(self.list_obj)

    def on_back(self):
        self.counter_obj = 0
        self.on_play()

    def on_play(self):
        self.canvas.plotSingle(self.list_obj[self.counter_obj])
        self.toolbar.setCount('%2d/%d' % (self.counter_obj + 1, len(self.list_obj)))
        self.toolbar.setTimeStamp(self.list_obj[self.counter_obj].getTimeStamp())
        self.counter_obj += 1

        if len(self.list_obj) <= self.counter_obj:
            self.counter_obj = len(self.list_obj) - 1
