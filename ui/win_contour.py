import numpy as np
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from structs.res import AppRes
from ui.dock_contour import DockContour
from ui.toolbar_contour import ToolbarContour
from widgets.charts import Contour, ChartNavigation


class WinContour(QMainWindow):

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res
        self.df = pd.DataFrame()

        self.setWindowTitle('Contour Map')

        toolbar = ToolbarContour(res)
        toolbar.provideFileName.connect(self.read_pickle)
        self.addToolBar(toolbar)

        self.dock = dock = DockContour(self.res)
        dock.requestContour.connect(self.on_plot)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        self.contour = contour = Contour(self.res)
        self.setCentralWidget(contour)

        self.navtoolbar = navtoolbar = ChartNavigation(contour)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

    def on_plot(self, dict_data: dict):
        """
        Contour Map のプロット
        :param dict_data:
        :return:
        """
        # print(dict_data['x'])
        # print(dict_data['y'])
        # print(dict_data['z'])
        self.contour.plot(dict_data)

    def read_pickle(self, pklfile: str):
        self.df = df = pd.read_pickle(pklfile)
        self.dock.setParams(df)
