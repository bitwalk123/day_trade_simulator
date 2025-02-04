from PySide6.QtWidgets import QMainWindow

from structs.res import AppRes
from ui.toolbar_explorer import ToolbarExplorer


class WinExplorer(QMainWindow):

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        self.setWindowTitle('最適パラメータ探索')

        toolbar = ToolbarExplorer(res)
        self.addToolBar(toolbar)