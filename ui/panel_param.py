import os

import pandas as pd
from PySide6.QtWidgets import QSizePolicy

from structs.res import AppRes
from widgets.container import Widget
from widgets.labels import (
    LabelFloat,
    LabelIntRaised,
    LabelTitleRaised,
    LabelValue,
)
from widgets.layouts import GridLayout


class PanelParam(Widget):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )

        # ----------------------------------
        #  パラメータ AF（加速因数）水準の読み込み
        # ----------------------------------
        file_json = 'af_params.json'
        df = pd.read_json(os.path.join(res.dir_config, file_json))

        # 水準テーブル用オブジェクト
        self.dict_obj = dict_obj = dict()
        self.counter_max = len(df)  # 水準数を保持

        # =====================================================================
        #  水準テーブル
        # =====================================================================
        layout = GridLayout()
        self.setLayout(layout)

        r = 0
        labNo = LabelTitleRaised('#')
        layout.addWidget(labNo, r, 0)

        labAFinit = LabelTitleRaised('AF init')
        layout.addWidget(labAFinit, r, 1)

        labAFstep = LabelTitleRaised('AF step')
        layout.addWidget(labAFstep, r, 2)

        labAFmax = LabelTitleRaised('AF max')
        layout.addWidget(labAFmax, r, 3)

        labTotal = LabelTitleRaised('合計損益')
        layout.addWidget(labTotal, r, 4)

        for i in range(len(df)):
            r += 1

            objNo = LabelIntRaised()
            objNo.setValue(r)
            dict_obj[r] = dict()
            layout.addWidget(objNo, r, 0)

            objAFinit = LabelFloat()
            objAFinit.setValue(df.at[r, 'af_init'])
            dict_obj[r]['af_init'] = objAFinit
            layout.addWidget(objAFinit, r, 1)

            objAFstep = LabelFloat()
            objAFstep.setValue(df.at[r, 'af_step'])
            dict_obj[r]['af_step'] = objAFstep
            layout.addWidget(objAFstep, r, 2)

            objAFmax = LabelFloat()
            objAFmax.setValue(df.at[r, 'af_max'])
            dict_obj[r]['af_max'] = objAFmax
            layout.addWidget(objAFmax, r, 3)

            objTotal = LabelValue()
            objTotal.setValue(0)
            dict_obj[r]['total'] = objTotal
            layout.addWidget(objTotal, r, 4)

    def getLevelMax(self) -> int:
        return self.counter_max

    def getAFinit(self, i: int) -> float:
        obj: LabelFloat = self.dict_obj[i + 1]['af_init']
        return obj.getValue()

    def getAFstep(self, i: int) -> float:
        obj: LabelFloat = self.dict_obj[i + 1]['af_step']
        return obj.getValue()

    def getAFmax(self, i: int) -> float:
        obj: LabelFloat = self.dict_obj[i + 1]['af_max']
        return obj.getValue()

    def getTotal(self, i: int) -> float:
        obj: LabelValue = self.dict_obj[i + 1]['total']
        return obj.getValue()

    def setTotal(self, i: int, total: float):
        """setTotal - 合計損益を対象ウィジェットに設定

        :param i:     カウンタは既にインクリメントされている（1 から始まる）。
        :param total: 合計損益
        :return:
        """
        obj: LabelValue = self.dict_obj[i]['total']
        return obj.setValue(total)
