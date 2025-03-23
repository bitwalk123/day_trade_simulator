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

        for i in range(1):
            r += 1

            objNo = LabelIntRaised()
            objNo.setValue(r)
            layout.addWidget(objNo, r, 0)

            objAFinit = LabelFloat()
            objAFinit.setValue(0)
            layout.addWidget(objAFinit, r, 1)

            objAFstep = LabelFloat()
            objAFstep.setValue(0)
            layout.addWidget(objAFstep, r, 2)

            objAFmax = LabelFloat()
            objAFmax.setValue(0)
            layout.addWidget(objAFmax, r, 3)

            objTotal = LabelValue()
            objTotal.setValue(0)
            layout.addWidget(objTotal, r, 4)
