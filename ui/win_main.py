import os

import pandas as pd
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import QMainWindow, QProgressBar

from funcs.conv import df_to_html
from structs.res import AppRes
from threads.simulator import WorkerSimulator
from ui.dock import DockMain
from ui.win_order_history import WinOrderHistory
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

        # チャートのサブタイトル書式
        self.af_param_format = 'AF: init = %.5f, step = %.5f, max = %.5f'

        # 注文履歴
        self.order_hist: WinOrderHistory | None = None  # 注文履歴
        self.df_order: pd.DataFrame | None = None
        self.column_format: list | None = None
        self.total_profit = 0

        # ### UI ##############################################################

        # ドック
        self.dock = dock = DockMain(res, dict_target)
        dock.requestOrderHistory.connect(self.on_order_history)
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
        dict_plot = dict()
        dict_plot['title'] = dict_target['title']
        dict_plot['subtitle'] = self.af_param_format % (
            dict_target['af_init'],
            dict_target['af_step'],
            dict_target['af_max']
        )
        dict_plot['tick'] = dict_target['tick']
        dict_plot['profit'] = pd.DataFrame()
        dict_plot['ylabel_tick'] = 'Price'
        dict_plot['ylabel_profit'] = 'Profit'
        # プロット
        canvas.plot(dict_plot)

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  注文履歴
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    def on_order_history(self):
        if self.df_order is None:
            return

        if self.order_hist is not None:
            self.order_hist.hide()
            self.order_hist.deleteLater()
        self.order_hist = WinOrderHistory(self.res, self.df_order, self.column_format, self.total_profit)
        self.order_hist.requestOrderHistoryHTML.connect(self.on_order_history_html)
        self.order_hist.show()

    def on_order_history_html(self):
        if self.df_order is None:
            return

        list_html = df_to_html(self.df_order, self.column_format, self.total_profit)

        home = os.path.expanduser("~")
        name_html = os.path.join(home, 'result.html')
        with open(name_html, mode='w') as f:
            f.writelines(list_html)

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  取引シミュレーション
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    def on_simulation_finished(self, dict_result: dict):
        """
        取引シミュレーションのスレッド処理終了
        :param dict_result:
        :return:
        """

        df_tick = dict_result['tick']
        df_profit = dict_result['profit']
        self.df_order = df_order = dict_result['order']
        self.column_format = dict_result['column_format']
        self.total_profit = total = dict_result['total']

        # プロットを更新
        dict_plot = dict()
        dict_plot['title'] = self.dict_target['title']
        dict_param = dict()
        self.dock.get_psar_af_param(dict_param)
        dict_plot['subtitle'] = self.af_param_format % (
            dict_param['af_init'],
            dict_param['af_step'],
            dict_param['af_max']
        )
        dict_plot['tick'] = df_tick
        dict_plot['profit'] = df_profit
        dict_plot['ylabel_tick'] = 'Price'
        dict_plot['ylabel_profit'] = 'Profit'

        self.canvas.plot(dict_plot)

        # 進捗をリセット
        self.pbar.reset()

        # タイマー状態
        self.dock.setStatus('停止')

        # 注文履歴の出力（暫定）
        self.on_order_history_html()

    def on_simulation_start(self, dict_info):
        """
        取引シミュレーションのスレッド処理開始
        :param dict_info:
        :return:
        """
        self.dock.setStatus('稼働中')

        sim = WorkerSimulator(dict_info)
        sim.positionOpen.connect(self.on_simulation_position_open)
        sim.positionClose.connect(self.on_simulation_position_close)
        sim.updateProfit.connect(self.on_simulation_update_profit)
        sim.updateSystemTime.connect(self.on_simulation_update_systemtime)
        sim.updateTickPrice.connect(self.on_simulation_update_tickprice)
        sim.threadFinished.connect(self.on_simulation_finished)
        self.threadpool.start(sim)

    def on_simulation_position_open(self, dict_position: dict):
        """
        新しい建玉の売買と値段
        :param dict_position:
        :return:
        """
        position = dict_position['position']
        price = dict_position['price']
        self.dock.setPosition(position, price)

    def on_simulation_position_close(self, total: float):
        """
        建玉返済による合計損益の更新
        :param total:
        :return:
        """
        self.dock.setPosition('無し', 0)
        self.dock.setTotal(total)

    def on_simulation_update_profit(self, dict_profit):
        """
        シミュレーションの更新された含み益
        :param dict_profit:
        :return:
        """
        self.dock.setProfit(dict_profit['profit'])
        self.dock.setProfitMax(dict_profit['profit_max'])

    def on_simulation_update_systemtime(self, time_str: str, progress: int):
        """
        シミュレーションの時刻と進捗度の更新
        :param time_str:
        :param progress:
        :return:
        """
        self.dock.setSystemTime(time_str)
        self.pbar.setValue(progress)

    def on_simulation_update_tickprice(self, time_str: str, price: float, trend: int):
        """
        ティックデータの時刻、株価およびトレンドの更新
        :param time_str:
        :param price:
        :param trend:
        :return:
        """
        self.dock.setTickPrice(time_str, price, trend)
