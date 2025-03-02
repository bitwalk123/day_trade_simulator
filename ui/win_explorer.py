import os

import pandas as pd
from PySide6.QtCore import QDate, Signal, QMargins, Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QScrollArea,
    QWidget,
)

from funcs.preprocs import prep_dataset, prep_result_df
from funcs.tide import get_yyyymmdd
from structs.res import AppRes
from ui.toolbar_explorer import ToolbarExplorer
from widgets.labels import LabelTitle, LabelTitle2, LabelValue
from widgets.spinbox import SpinBox


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

        self.dict_low = dict()
        self.dict_high = dict()

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

            lab_default = LabelValue()
            lab_default.setValue(self.params[key], False)
            lab_default.setMinimumWidth(50)
            layout.addWidget(lab_default, r, 1)

            match key:
                case 'period_max':
                    self.dict_low[key] = 3
                    self.dict_high[key] = 7
                case 'factor_losscut_1':
                    self.dict_low[key] = 0
                    self.dict_high[key] = 5
                case 'factor_losscut_2':
                    self.dict_low[key] = 0
                    self.dict_high[key] = 5
                case 'factor_profit_1':
                    self.dict_low[key] = 5
                    self.dict_high[key] = 10
                case 'threshold_profit_1':
                    self.dict_low[key] = 5
                    self.dict_high[key] = 9

            lab_low = SpinBox()
            lab_low.setValue(self.dict_low[key])

            lab_high = SpinBox()
            lab_high.setValue(self.dict_high[key])

            lab_inc = LabelValue()
            lab_inc.setValue(1, False)
            lab_inc.setMinimumWidth(50)

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

        print('date; %s.' % str(self.qdate))
        self.dict_target = prep_dataset(info, self.qdate, self.res)

        self.list_params = list()
        params = self.params.copy()
        self.idx = 0

        key_1 = 'period_max'
        for value_1 in range(self.dict_low[key_1], self.dict_high[key_1] + 1):
            params[key_1] = value_1

            key_2 = 'factor_losscut_1'
            for value_2 in range(self.dict_low[key_2], self.dict_high[key_2] + 1):
                params[key_2] = value_2

                key_3 = 'factor_losscut_2'
                for value_3 in range(self.dict_low[key_3], self.dict_high[key_3] + 1):
                    params[key_3] = value_3

                    key_4 = 'factor_profit_1'
                    for value_4 in range(self.dict_low[key_4], self.dict_high[key_4] + 1):
                        params[key_4] = value_4

                        key_5 = 'threshold_profit_1'
                        for value_5 in range(self.dict_low[key_5], self.dict_high[key_5] + 1):
                            params[key_5] = value_5

                            self.list_params.append(params.copy())

        self.df_result = prep_result_df(self.params)
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
