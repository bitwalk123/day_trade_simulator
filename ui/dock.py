from PySide6.QtCore import QMargins, Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QGridLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelString,
    LabelTime,
    LabelTitle,
    LabelValue,
)


class DockSimulator(QDockWidget):
    simStarted = Signal(dict)

    def __init__(self):
        super().__init__()
        self.dict_target = dict()
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
        lab000 = LabelFlat('【対象銘柄】')
        layout.addWidget(lab000, r, 0)

        r += 1
        lab010 = LabelTitle('銘柄コード')
        layout.addWidget(lab010, r, 0)

        self.objCode = lab011 = LabelString()
        layout.addWidget(lab011, r, 1)

        r += 1
        lab020 = LabelFlat('【現在値】')
        layout.addWidget(lab020, r, 0)

        r += 1
        lab030 = LabelTitle('現在日付')
        layout.addWidget(lab030, r, 0)

        self.objDate = lab031 = LabelDate()
        layout.addWidget(lab031, r, 1)

        r += 1
        lab040 = LabelTitle('システム時刻')
        layout.addWidget(lab040, r, 0)

        self.objSystemTime = lab041 = LabelTime()
        layout.addWidget(lab041, r, 1)

        r += 1
        lab050 = LabelTitle('現在値詳細時刻')
        layout.addWidget(lab050, r, 0)

        self.objTickTime = lab051 = LabelTime()
        layout.addWidget(lab051, r, 1)

        r += 1
        self.objTickPrice = lab060 = LabelTitle('現在値')
        layout.addWidget(lab060, r, 0)

        lab061 = LabelValue()
        layout.addWidget(lab061, r, 1)

        r += 1
        lab070 = LabelFlat('【ティック】')
        layout.addWidget(lab070, r, 0)

        r += 1
        lab080 = LabelTitle('タイマー状態')
        layout.addWidget(lab080, r, 0)

        lab081 = LabelString()
        layout.addWidget(lab081, r, 1)

        r += 1
        lab090 = LabelFlat('【取引】')
        layout.addWidget(lab090, r, 0)

        r += 1
        lab100 = LabelTitle('呼値')
        layout.addWidget(lab100, r, 0)

        self.objTickPrice = lab101 = LabelValue()
        layout.addWidget(lab101, r, 1)

        r += 1
        lab110 = LabelTitle('建玉価格')
        layout.addWidget(lab110, r, 0)

        lab111 = LabelValue()
        layout.addWidget(lab111, r, 1)

        r += 1
        lab120 = LabelTitle('売買単位')
        layout.addWidget(lab120, r, 0)

        self.objUnit = lab121 = LabelValue()
        layout.addWidget(lab121, r, 1)

        r += 1
        lab130 = LabelTitle('含み損益')
        layout.addWidget(lab130, r, 0)

        lab131 = LabelValue()
        layout.addWidget(lab131, r, 1)

        r += 1
        lab140 = LabelTitle('最大含み益')
        layout.addWidget(lab140, r, 0)

        lab141 = LabelValue()
        layout.addWidget(lab141, r, 1)

        r += 1
        lab150 = LabelTitle('トレンド')
        layout.addWidget(lab150, r, 0)

        lab151 = LabelValue()
        layout.addWidget(lab151, r, 1)

        r += 1
        lab160 = LabelTitle('合計損益')
        layout.addWidget(lab160, r, 0)

        lab161 = LabelValue()
        layout.addWidget(lab161, r, 1)

        r += 1
        base_control = QWidget()
        layout.addWidget(base_control, r, 0, 1, 2)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(QMargins(0, 20, 0, 0))
        base_control.setLayout(vbox)

        self.btnStart = but_start = QPushButton('START')
        but_start.setFixedHeight(40)
        but_start.clicked.connect(self.on_start)
        but_start.setDisabled(True)
        vbox.addWidget(but_start)

    def setInit(self, dict_target: dict):
        self.dict_target = dict_target

        self.objCode.setText(dict_target['code'])
        self.objDate.setText(dict_target['date_format'])
        self.objTickPrice.setValue(dict_target['tick_price'])
        self.objUnit.setValue(100, False)

        self.btnStart.setEnabled(True)

    def on_start(self):
        self.simStarted.emit(self.dict_target)

    def updateSystemTime(self, time_str: str):
        self.objSystemTime.setText(time_str)

    def updateTickPrice(self, time_str:str, price:float):
        self.objTickTime.setText(time_str)
        self.objTickPrice.setValue(price)