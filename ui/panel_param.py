from PySide6.QtWidgets import QSizePolicy

from structs.res import AppRes
from widgets.container import Widget
from widgets.labels import (
    LabelFloat,
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

        layout = GridLayout()
        self.setLayout(layout)

        r = 0
        labAFinit = LabelTitleRaised('AF init')
        layout.addWidget(labAFinit, r, 0)

        labAFstep = LabelTitleRaised('AF step')
        layout.addWidget(labAFstep, r, 1)

        labAFmax = LabelTitleRaised('AF max')
        layout.addWidget(labAFmax, r, 2)

        labTotal = LabelTitleRaised('合計損益')
        layout.addWidget(labTotal, r, 3)

        self.af_init = list()
        self.af_step = list()
        self.af_max = list()
        self.total = list()

        for i in range(1):
            r += 1

            objAFinit = LabelFloat()
            objAFinit.setValue(0)
            layout.addWidget(objAFinit, r, 0)

            objAFstep = LabelFloat()
            objAFstep.setValue(0)
            layout.addWidget(objAFstep, r, 1)

            objAFmax = LabelFloat()
            objAFmax.setValue(0)
            layout.addWidget(objAFmax, r, 2)

            objTotal = LabelValue()
            objTotal.setValue(0)
            layout.addWidget(objTotal, r, 3)

            """
            self.af_init.append(objAFinit)
            self.af_step.append(objAFstep)
            self.af_max.append(objAFmax)
            self.total.append(objTotal)
            """
