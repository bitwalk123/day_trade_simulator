import os

import pandas as pd
from PySide6.QtCore import QDate, Signal, QMargins, Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QScrollArea,
    QWidget,
)

from func.preprocs import prepDataset, prepResultDF
from func.tide import get_yyyymmdd
from structs.res import AppRes
from ui.toolbar_explorer import ToolbarExplorer
from widgets.labels import LabelTitle, LabelValue2, LabelTitle2
from widgets.spinbox import SpinBox, DoubleSpinBox


class WinExplorer(QMainWindow):
    requestAutoSim = Signal(dict, dict)

    def __init__(self, res: AppRes, params: dict):
        super().__init__()
        self.res = res
        # デフォルトのシミュレーション・パラメータ
        self.params = params
        self.df_result: pd.DataFrame | None = None
        self.qdate: QDate | None = None

        self.dict_target = dict()
        self.list_params = list()
        self.idx = 0

        self.setWindowTitle('最適パラメータ探索')
        self.resize(600, 400)

        toolbar = ToolbarExplorer(res)
        toolbar.playClicked.connect(self.on_start)
        toolbar.qdateSelected.connect(self.on_date)
        self.addToolBar(toolbar)

        sa = QScrollArea()
        sa.setWidgetResizable(True)
        self.setCentralWidget(sa)

        base = QWidget()
        sa.setWidget(base)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        base.setLayout(layout)

        r = 0
        col_title_1 = LabelTitle2('parameter')
        layout.addWidget(col_title_1, r, 0)
        col_title_2 = LabelTitle2('default')
        layout.addWidget(col_title_2, r, 1)
        col_title_3 = LabelTitle2('low')
        layout.addWidget(col_title_3, r, 2)
        col_title_4 = LabelTitle2('high')
        layout.addWidget(col_title_4, r, 3)
        col_title_5 = LabelTitle2('inc')
        layout.addWidget(col_title_5, r, 4)

        r += 1
        for key in self.params.keys():
            lab_name = LabelTitle(key)
            layout.addWidget(lab_name, r, 0)
            if key == 'threshold_profit_1':
                flag = True
            else:
                flag = False

            lab_default = LabelValue2()
            lab_default.setValue(self.params[key], flag)
            lab_default.setMinimumWidth(50)
            layout.addWidget(lab_default, r, 1)

            if flag:
                lab_low = DoubleSpinBox()
                lab_high = DoubleSpinBox()
                lab_inc = DoubleSpinBox()
                lab_low.setValue(0.1)
                lab_high.setValue(0.9)
                lab_inc.setValue(0.05)
            else:
                lab_low = SpinBox()
                lab_high = SpinBox()
                match key:
                    case 'period_max':
                        lab_low.setValue(2)
                        lab_high.setValue(10)
                    case 'factor_profit_1':
                        lab_low.setValue(3)
                        lab_high.setValue(15)
                    case _:
                        lab_low.setValue(0)
                        lab_high.setValue(10)

                lab_inc = SpinBox()
                lab_inc.setValue(1)

            layout.addWidget(lab_low, r, 2)
            layout.addWidget(lab_high, r, 3)
            layout.addWidget(lab_inc, r, 4)

            r += 1

        base.setFixedSize(self.sizeHint())

    def on_date(self, qdate: QDate):
        self.qdate = qdate
        print('selected %s.' % str(self.qdate))

    def on_start(self):
        info = dict()
        info['name'] = '三菱ＵＦＪフィナンシャルＧ'
        info['code'] = '8306'
        info['symbol'] = '8306.T'
        info['price_delta_min'] = 0.5
        info['unit'] = 100

        # qdate = QDate(2025, 1, 30)

        print('date; %s.' % str(self.qdate))
        self.dict_target = prepDataset(info, self.qdate, self.res)

        self.list_params = list()
        params = self.params.copy()
        self.idx = 0

        for value_1 in range(3, 8):
            params['period_max'] = value_1
            for value_2 in range(0, 6):
                params['factor_losscut_1'] = value_2
                for value_3 in range(0, 6):
                    params['factor_losscut_2'] = value_3
                    for value_4 in range(5, 12):
                        params['factor_profit_1'] = value_4
                        for value_5 in range(6, 10):
                            params['threshold_profit_1'] = value_5
                            params0 = params.copy()
                            self.list_params.append(params0)

        self.df_result = prepResultDF(self.params)
        self.do_auto_sim()

    def do_auto_sim(self):
        if self.idx < len(self.list_params):
            params = self.list_params[self.idx]
            self.requestAutoSim.emit(self.dict_target, params)
            self.idx += 1
        else:
            total_max = self.df_result['total'].max()
            print(self.df_result[self.df_result['total'] == total_max])
            file_pkl = os.path.join(
                self.res.dir_result,
                'result_%s.pkl' % get_yyyymmdd(self.qdate)
            )
            self.df_result.to_pickle(file_pkl)
            print('Completed!')

    def appendResult(self, result: dict):
        """
        シミュレーション結果をデータフレームの末尾の行に追加する
        :param result:
        :return:
        """
        print('%d/%d' % (self.idx, len(self.list_params)))
        r = len(self.df_result)
        for key in result.keys():
            self.df_result.at[r, key] = result[key]
        self.do_auto_sim()
