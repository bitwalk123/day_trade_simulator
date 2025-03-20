from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import QMainWindow, QProgressBar

from funcs.plots import get_dict4plot
from structs.res import AppRes
from threads.simulator import WorkerSimulator
from ui.dock import DockMain
from widgets.charts import Canvas, ChartNavigation


class WinMain(QMainWindow):
    def __init__(
            self,
            res: AppRes,
            dict_target: dict,
            threadpool: QThreadPool,
            pbar: QProgressBar,
    ):
        super().__init__()
        self.res = res
        self.dict_target = dict_target
        self.threadpool = threadpool
        self.pbar = pbar

        # ドック
        self.dock = dock = DockMain(res, dict_target)
        dock.requestSimulationStart.connect(self.on_simulation_start)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # メイン・ウィンドウ
        self.canvas = canvas = Canvas(res)
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
        dict_plot = get_dict4plot(dict_target['title'], dict_target['tick'])
        canvas.plot(dict_plot)

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  取引シミュレーション
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    def on_simulation_start(self, dict_info):
        self.dock.setStatus('稼働中')
        sim = WorkerSimulator(dict_info)
        sim.updateSystemTime.connect(self.on_simulation_update_systemtime)
        sim.updateTickPrice.connect(self.on_simulation_update_tickprice)
        sim.threadFinished.connect(self.on_simulation_finished)
        self.threadpool.start(sim)

    def on_simulation_update_systemtime(self, time_str: str, progress: int):
        self.dock.setSystemTime(time_str)
        self.pbar.setValue(progress)

    def on_simulation_update_tickprice(self, time_str: str, price: float, trend: int):
        self.dock.setTickPrice(time_str, price, trend)

    def on_simulation_finished(self, dict_result:dict):
        """
        シミュレーションのスレッド終了
        :param df:
        :return:
        """

        df_tick = dict_result['tick']
        df_profit = dict_result['profit']
        df_order = dict_result['order']
        total = dict_result['total']

        #print(df_profit)
        #print(df_order)
        #print(total)

        # プロットを更新
        dict_plot = get_dict4plot(self.dict_target['title'], df_tick, df_profit)
        self.canvas.plot(dict_plot)

        # 進捗をリセット
        self.pbar.reset()

        # タイマー状態
        self.dock.setStatus('停止')
