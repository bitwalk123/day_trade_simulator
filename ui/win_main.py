from PySide6.QtWidgets import QMainWindow

from structs.res import AppRes
from widgets.charts import Canvas


class WinMain(QMainWindow):
    def __init__(self, res: AppRes, dict_target: dict):
        super().__init__()
        self.res = res
        self.dict_darget = dict_target

        canvas = Canvas(res)
        self.setCentralWidget(canvas)

        canvas.plot(dict_target)