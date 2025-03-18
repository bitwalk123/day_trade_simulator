from PySide6.QtCore import QMargins, Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QGridLayout,
    QSizePolicy,
    QVBoxLayout,
    QWidget, QPushButton,
)

from structs.res import AppRes
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelString,
    LabelTime,
    LabelTitle,
    LabelValue,
    LabelUnit,
)


class DockMain(QDockWidget):
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # UI
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        self.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )

        base = QWidget()
        base.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.setWidget(base)

        layout = QGridLayout()
        layout.setSpacing(0)
        base.setLayout(layout)

        r = 0
        labSystem = LabelFlat('【システム】')
        layout.addWidget(labSystem, r, 0)

        r += 1
        labSystemTime = LabelTitle('システム時刻')
        layout.addWidget(labSystemTime, r, 0)

        self.objSystemTime = objSystemTime = LabelTime()
        layout.addWidget(objSystemTime, r, 1)

        r += 1
        labStatus = LabelTitle('タイマー状態')
        layout.addWidget(labStatus, r, 0)

        self.objStatus = objStatus = LabelString()
        layout.addWidget(objStatus, r, 1)

        r += 1
        labTargetCode = LabelFlat('【対象銘柄】')
        layout.addWidget(labTargetCode, r, 0)

        r += 1
        labCode = LabelTitle('銘柄コード')
        layout.addWidget(labCode, r, 0)

        self.objCode = objCode = LabelString()
        layout.addWidget(objCode, r, 1)

        r += 1
        labDate = LabelTitle('現在日付')
        layout.addWidget(labDate, r, 0)

        self.objDate = objDate = LabelDate()
        layout.addWidget(objDate, r, 1)

        r += 1
        labTickTime = LabelTitle('現在値詳細時刻')
        layout.addWidget(labTickTime, r, 0)

        self.objTickTime = objTickTime = LabelTime()
        layout.addWidget(objTickTime, r, 1)

        r += 1
        labTickPrice = LabelTitle('現在値')
        layout.addWidget(labTickPrice, r, 0)

        self.objTickPrice = objTickPrice = LabelValue()
        layout.addWidget(objTickPrice, r, 1)

        unitTickPrice = LabelUnit('円')
        layout.addWidget(unitTickPrice, r, 2)

        r += 1
        labTickPriceMin = LabelTitle('呼値')
        layout.addWidget(labTickPriceMin, r, 0)

        self.objTickPriceMin = objTickPriceMin = LabelValue()
        layout.addWidget(objTickPriceMin, r, 1)

        unitTickPriceMin = LabelUnit('円')
        layout.addWidget(unitTickPriceMin, r, 2)

        r += 1
        labTransaction = LabelFlat('【取引】')
        layout.addWidget(labTransaction, r, 0)

        r += 1
        labPosition = LabelTitle('建玉')
        layout.addWidget(labPosition, r, 0)

        self.objPosition = objPosition = LabelString()
        objPosition.setText('無し')
        layout.addWidget(objPosition, r, 1)

        r += 1
        labPositionPrice = LabelTitle('建玉価格')
        layout.addWidget(labPositionPrice, r, 0)

        self.objPositionPrice = objPositionPrice = LabelValue()
        layout.addWidget(objPositionPrice, r, 1)

        unitPositionPrice = LabelUnit('円')
        layout.addWidget(unitPositionPrice, r, 2)

        r += 1
        labUnit = LabelTitle('売買単位')
        layout.addWidget(labUnit, r, 0)

        self.objUnit = objUnit = LabelValue()
        layout.addWidget(objUnit, r, 1)

        unitUnit = LabelUnit('株')
        layout.addWidget(unitUnit, r, 2)

        r += 1
        labProfit = LabelTitle('含み損益')
        layout.addWidget(labProfit, r, 0)

        self.objProfit = objProfit = LabelValue()
        layout.addWidget(objProfit, r, 1)

        unitProfit = LabelUnit('円')
        layout.addWidget(unitProfit, r, 2)

        r += 1
        labProfitMax = LabelTitle('最大含み益')
        layout.addWidget(labProfitMax, r, 0)

        self.objProfitMax = objProfitMax = LabelValue()
        layout.addWidget(objProfitMax, r, 1)

        unitProfitMax = LabelUnit('円')
        layout.addWidget(unitProfitMax, r, 2)

        r += 1
        labTrend = LabelTitle('トレンド')
        layout.addWidget(labTrend, r, 0)

        self.objTrend = objTrend = LabelValue()
        layout.addWidget(objTrend, r, 1)

        r += 1
        labTotal = LabelTitle('合計損益')
        layout.addWidget(labTotal, r, 0)

        self.objTotal = objTotal = LabelValue()
        layout.addWidget(objTotal, r, 1)

        unitTotal = LabelUnit('円')
        layout.addWidget(unitTotal, r, 2)

        r += 1
        labParameter = LabelFlat('【パラメータ】')
        layout.addWidget(labParameter, r, 0)

        r += 1
        labParameter = LabelFlat('Parabolic SAR')
        labParameter.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(labParameter, r, 0)

        r += 1
        labAFinit = LabelTitle('AF（初期値）')
        layout.addWidget(labAFinit, r, 0)

        self.objAFinit = objAFinit = LabelValue()
        layout.addWidget(objAFinit, r, 1, 1, 2)

        r += 1
        labAFstep = LabelTitle('AF（ステップ）')
        layout.addWidget(labAFstep, r, 0)

        self.objAFstep = objAFstep = LabelValue()
        layout.addWidget(objAFstep, r, 1, 1, 2)

        r += 1
        labAFmax = LabelTitle('AF（最大値）')
        layout.addWidget(labAFmax, r, 0)

        self.objAFmax = objAFmax = LabelValue()
        layout.addWidget(objAFmax, r, 1, 1, 2)

        r += 1
        base_control = QWidget()
        layout.addWidget(base_control, r, 0, 1, 3)

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(QMargins(0, 20, 0, 0))
        base_control.setLayout(vbox)

        self.btnStart = but_start = QPushButton('START')
        but_start.setFixedHeight(50)
        but_start.clicked.connect(self.on_start)
        but_start.setDisabled(True)
        vbox.addWidget(but_start)

    def on_start(self):
        pass
