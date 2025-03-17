from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from structs.res import AppRes
from widgets.charts import Canvas, ChartNavigation


class WinMain(QMainWindow):
    def __init__(self, res: AppRes, dict_target: dict):
        super().__init__()
        self.res = res
        self.dict_darget = dict_target

        canvas = Canvas(res)
        self.setCentralWidget(canvas)

        self.navtoolbar = navtoolbar = ChartNavigation(canvas)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

        canvas.plot(dict_target)