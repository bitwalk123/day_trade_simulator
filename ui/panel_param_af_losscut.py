import os

import pandas as pd
from PySide6.QtWidgets import QSizePolicy

from structs.res import AppRes
from widgets.container import Widget, ScrollAreaVertical
from widgets.labels import (
    LabelFloat,
    LabelInt,
    LabelIntRaised,
    LabelTitleRaised,
    LabelValue,
)
from widgets.layouts import GridLayout


class PanelParam(ScrollAreaVertical):
    def __init__(self, res: AppRes):
        super().__init__()
        # ----------------------------------
        #  パラメータ AF（加速因数）水準の読み込み
        # ----------------------------------
        file_json = 'doe_af_losscut.json'
        self.df = df = pd.read_json(os.path.join(res.dir_config, file_json))
        df['Total'] = 0

        # 水準テーブル用オブジェクト
        self.dict_obj = dict_obj = dict()
        self.counter_max = len(df)  # 水準数を保持

        # =====================================================================
        #  水準テーブル
        # =====================================================================
        base = Widget()
        self.setWidget(base)
        base.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )
        layout = GridLayout()
        base.setLayout(layout)

        r = 0
        labNo = LabelTitleRaised('#')
        layout.addWidget(labNo, r, 0)

        labAFinit = LabelTitleRaised('AF init')
        layout.addWidget(labAFinit, r, 1)

        labAFstep = LabelTitleRaised('AF step')
        layout.addWidget(labAFstep, r, 2)

        labAFmax = LabelTitleRaised('AF max')
        layout.addWidget(labAFmax, r, 3)

        labLosscut = LabelTitleRaised('損切因数')
        layout.addWidget(labLosscut, r, 4)

        labTotal = LabelTitleRaised('合計損益')
        layout.addWidget(labTotal, r, 5)

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

            objLosscut = LabelInt()
            objLosscut.setValue(df.at[r, 'factor_losscut'])
            dict_obj[r]['factor_losscut'] = objLosscut
            layout.addWidget(objLosscut, r, 4)

            objTotal = LabelValue()
            objTotal.setValue(0)
            dict_obj[r]['total'] = objTotal
            layout.addWidget(objTotal, r, 5)

        # print(dict_obj)

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

    def getLosscut(self, i: int) -> float:
        obj: LabelInt = self.dict_obj[i + 1]['factor_losscut']
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
        obj.setValue(total)
        self.df.at[i, 'Total'] = total

    def getResult(self, name_html: str):
        list_html = list()

        # table
        list_html.append('<table class="simple">\n')

        # header
        list_html.append('<thead>\n')
        list_html.append('<tr>\n')
        for colname in ['#', 'AF init', 'AF step', 'AF max', 'Losscut', 'Total']:
            list_html.append('<th nowrap>%s</th>\n' % colname)

        list_html.append('</tr>\n')
        list_html.append('</thead>\n')
        # body
        list_html.append('<tbody>\n')
        rows = len(self.df)
        for r in range(rows):
            list_html.append('<tr>\n')
            # Run
            list_html.append('<td nowrap style="text-align: right;">%d</td>\n' % (r + 1))
            # AF init
            af_init = self.df.at[r + 1, 'af_init']
            list_html.append('<td nowrap style="text-align: right;">%.5f</td>\n' % af_init)
            # AF step
            af_step = self.df.at[r + 1, 'af_step']
            list_html.append('<td nowrap style="text-align: right;">%.5f</td>\n' % af_step)
            # AF max
            af_max = self.df.at[r + 1, 'af_max']
            list_html.append('<td nowrap style="text-align: right;">%.5f</td>\n' % af_max)
            # Losscut Factor
            factor_losscut = self.df.at[r + 1, 'factor_losscut']
            list_html.append('<td nowrap style="text-align: right;">%d</td>\n' % factor_losscut)
            # Total
            total = self.df.at[r + 1, 'Total']
            list_html.append('<td nowrap style="text-align: right;">{:,}</td>\n'.format(int(total)))

            list_html.append('</tr>\n')

        list_html.append('</tbody>\n')

        # end of table
        list_html.append('</table>\n')

        with open(name_html, mode='w') as f:
            f.writelines(list_html)
