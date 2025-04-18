import os

import pandas as pd
from PySide6.QtWidgets import QSizePolicy

from structs.res import AppRes
from widgets.container import Widget, ScrollAreaVertical
from widgets.labels import (
    LabelFloat,
    LabelIntRaised,
    LabelTitleRaised,
    LabelValue,
)
from widgets.layouts import GridLayout


class PanelParam(ScrollAreaVertical):
    def __init__(self, res: AppRes, file_json: str):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )

        # ----------------------------------
        #  パラメータ AF（加速因数）水準の読み込み
        # ----------------------------------
        # file_json = 'doe_af.json'
        self.df = df = pd.read_json(os.path.join(res.dir_config, file_json))
        self.coltotal = coltotal = 'total'
        df[coltotal] = 0

        # 水準テーブル用オブジェクト
        self.dict_obj = dict_obj = dict()
        self.counter_max = len(df)  # 水準数を保持

        # =====================================================================
        #  水準テーブル
        # =====================================================================
        base = Widget()
        self.setWidget(base)
        layout = GridLayout()
        base.setLayout(layout)

        r = 0
        labNo = LabelTitleRaised('#')
        layout.addWidget(labNo, r, 0)

        for c, colname in enumerate(self.df.columns):
            labAFinit = LabelTitleRaised(colname)
            layout.addWidget(labAFinit, r, c + 1)

        for i in range(len(self.df)):
            r += 1

            objNo = LabelIntRaised()
            objNo.setValue(r)
            dict_obj[r] = dict()
            layout.addWidget(objNo, r, 0)

            for c, colname in enumerate(self.df.columns):
                if colname == self.coltotal:
                    obj = LabelValue()
                else:
                    obj = LabelFloat()
                obj.setValue(df.at[r, colname])
                dict_obj[r][colname] = obj
                layout.addWidget(obj, r, c + 1)

    def clearTotal(self):
        for r in range(len(self.df)):
            self.setTotal(r + 1, 0.0)

    def getLevelMax(self) -> int:
        return self.counter_max

    def getAFinit(self, i: int) -> float:
        obj: LabelFloat = self.dict_obj[i]['af_init']
        return obj.getValue()

    def getAFstep(self, i: int) -> float:
        obj: LabelFloat = self.dict_obj[i]['af_step']
        return obj.getValue()

    def getAFmax(self, i: int) -> float:
        obj: LabelFloat = self.dict_obj[i]['af_max']
        return obj.getValue()

    def getTotal(self, i: int) -> float:
        obj: LabelValue = self.dict_obj[i][self.coltotal]
        return obj.getValue()

    def setTotal(self, i: int, total: float):
        """setTotal - 合計損益を対象ウィジェットに設定

        :param i:     カウンタは既にインクリメントされている（1 から始まる）。
        :param total: 合計損益
        :return:
        """
        obj: LabelValue = self.dict_obj[i][self.coltotal]
        obj.setValue(total)
        self.df.at[i, self.coltotal] = total

    def getResult(self, name_html: str):
        list_html = list()

        # table
        list_html.append('<table class="simple">\n')

        # header
        list_html.append('<thead>\n')
        list_html.append('<tr>\n')

        list_html.append('<th nowrap>#</th>\n')
        for colname in self.df.columns:
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

            for c, colname in enumerate(self.df.columns):
                value = self.df.at[r + 1, colname]
                if colname == self.coltotal:
                    list_html.append('<td nowrap style="text-align: right;">%d</td>\n' % int(value))
                else:
                    list_html.append('<td nowrap style="text-align: right;">%.5f</td>\n' % value)

            list_html.append('</tr>\n')

        list_html.append('</tbody>\n')

        # end of table
        list_html.append('</table>\n')

        with open(name_html, mode='w') as f:
            f.writelines(list_html)
