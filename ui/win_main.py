from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from funcs.plots import get_dict4plot
from structs.res import AppRes
from ui.dock import DockMain
from widgets.charts import Canvas, ChartNavigation


class WinMain(QMainWindow):
    def __init__(self, res: AppRes, dict_target: dict):
        super().__init__()
        self.res = res
        self.dict_darget = dict_target

        # ドック
        self.dock = dock = DockMain(self.res)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # メイン・ウィンドウ
        canvas = Canvas(res)
        # デフォルトの保存用プロット画像のファイル名
        canvas.get_default_filename = lambda: '%s_%s.png' % (
            dict_target['code'],
            dict_target['date'].replace('-', ''),
        )
        self.setCentralWidget(canvas)

        self.navtoolbar = navtoolbar = ChartNavigation(canvas)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

        # チャートに渡す情報を dict_target にせずに、敢えて必要分のみを dict_plot へ移して渡す。
        # これは、パラメータを変更して再描画するために自由度を確保するため。
        dict_plot = get_dict4plot(dict_target['tick'], dict_target['title'])
        canvas.plot(dict_plot)
