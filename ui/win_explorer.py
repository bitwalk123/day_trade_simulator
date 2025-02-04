import os

from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import QMainWindow

from func.io import read_json
from func.preprocs import prepDataset
from structs.res import AppRes
from ui.toolbar_explorer import ToolbarExplorer


class WinExplorer(QMainWindow):
    requestAutoSim = Signal(dict, dict)

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        self.setWindowTitle('最適パラメータ探索')

        toolbar = ToolbarExplorer(res)
        toolbar.playClicked.connect(self.on_start)
        self.addToolBar(toolbar)

    def on_start(self):
        info = dict()
        info['name'] = '三菱ＵＦＪフィナンシャルＧ'
        info['code'] = '8306'
        info['symbol'] = '8306.T'
        info['price_delta_min'] = 0.5
        info['unit'] = 100

        qdate = QDate(2025, 2, 4)

        dict_target = prepDataset(info, qdate, self.res)

        # 暫定的にシミュレーション・パラメータ（辞書）の読み込んで使用
        json_params = os.path.join(self.res.dir_config, 'params.json')
        params = read_json(json_params)

        # データフレーム準備完了シグナル
        self.requestAutoSim.emit(dict_target, params)
