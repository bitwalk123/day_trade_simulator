import os

from PySide6.QtCore import QMargins, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDockWidget,
    QGridLayout,
    QHBoxLayout,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from funcs.io import read_json
from structs.res import AppRes
from ui.win_contour import WinContour
from ui.win_explorer import WinExplorer
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelString,
    LabelTime,
    LabelTitle,
    LabelUnit,
    LabelValue,
)
from widgets.container import PadH


class DockSimulator(QDockWidget):
    requestOrderHistory = Signal()
    requestOrderHistoryHTML = Signal()
    requestOverlayAnalysis = Signal(dict)
    requestSimulationStart = Signal(dict, dict)
    requestAutoSimStart = Signal(dict, dict)

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res
        self.dict_target = dict()

        # シミュレーション・パラメータ（辞書）の読み込み
        json_params = os.path.join(res.dir_config, 'params.json')
        self.params = read_json(json_params)

        # 鳥瞰図用ウィンドウ
        self.contour: WinContour | None = None

        # 最適パラメータ探索用ウィンドウ
        self.explorer: WinExplorer | None = None

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
        lab060 = LabelTitle('現在値')
        layout.addWidget(lab060, r, 0)

        self.objTickPrice = lab061 = LabelValue()
        layout.addWidget(lab061, r, 1)

        r += 1
        lab070 = LabelFlat('【ティック】')
        layout.addWidget(lab070, r, 0)

        r += 1
        lab080 = LabelTitle('タイマー状態')
        layout.addWidget(lab080, r, 0)

        self.objStatus = lab081 = LabelString()
        layout.addWidget(lab081, r, 1)

        r += 1
        lab090 = LabelFlat('【取引】')
        layout.addWidget(lab090, r, 0)

        r += 1
        lab100 = LabelTitle('呼値')
        layout.addWidget(lab100, r, 0)

        self.objPriceDeltaMin = lab101 = LabelValue()
        layout.addWidget(lab101, r, 1)

        lab102 = LabelUnit('円')
        layout.addWidget(lab102, r, 2)

        r += 1
        lab110 = LabelTitle('建玉価格')
        layout.addWidget(lab110, r, 0)

        self.objPricePos = lab111 = LabelValue()
        layout.addWidget(lab111, r, 1)

        self.objBuySell = lab112 = LabelUnit('無し')
        layout.addWidget(lab112, r, 2)

        r += 1
        lab120 = LabelTitle('売買単位')
        layout.addWidget(lab120, r, 0)

        self.objUnit = lab121 = LabelValue()
        layout.addWidget(lab121, r, 1)

        lab122 = LabelUnit('株')
        layout.addWidget(lab122, r, 2)

        r += 1
        lab130 = LabelTitle('含み損益')
        layout.addWidget(lab130, r, 0)

        self.objProfit = lab131 = LabelValue()
        layout.addWidget(lab131, r, 1)

        lab132 = LabelUnit('円')
        layout.addWidget(lab132, r, 2)

        r += 1
        lab140 = LabelTitle('最大含み益')
        layout.addWidget(lab140, r, 0)

        self.objProfitMax = lab141 = LabelValue()
        layout.addWidget(lab141, r, 1)

        lab142 = LabelUnit('円')
        layout.addWidget(lab142, r, 2)

        r += 1
        lab150 = LabelTitle('トレンド')
        layout.addWidget(lab150, r, 0)

        self.objTrend = lab151 = LabelValue()
        layout.addWidget(lab151, r, 1)

        r += 1
        lab160 = LabelTitle('合計損益')
        layout.addWidget(lab160, r, 0)

        self.objTotal = lab161 = LabelValue()
        layout.addWidget(lab161, r, 1)

        lab162 = LabelUnit('円')
        layout.addWidget(lab162, r, 2)

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

        self.progress = progress = QProgressBar()
        vbox.addWidget(progress)

        hbar = QWidget()
        vbox.addWidget(hbar)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        hbar.setLayout(hbox)

        hpad = PadH()
        hbox.addWidget(hpad)

        but_contour = QPushButton()
        but_contour.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'contour.png'))
        )
        but_contour.setToolTip('鳥瞰図による最適領域チェック')
        but_contour.clicked.connect(self.on_contour)
        hbox.addWidget(but_contour)

        but_explorer = QPushButton()
        but_explorer.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'explore.png'))
        )
        but_explorer.setToolTip('最適パラメータの探索')
        but_explorer.clicked.connect(self.on_explorer)
        hbox.addWidget(but_explorer)

        but_overlay = QPushButton()
        but_overlay.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'overlay.png'))
        )
        but_overlay.setToolTip('重ね合わせ')
        but_overlay.clicked.connect(self.on_overlay)
        hbox.addWidget(but_overlay)

        but_html = QPushButton()
        but_html.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'html.png'))
        )
        but_html.setToolTip('売買履歴（HTML出力）')
        but_html.clicked.connect(self.on_order_history_html)
        hbox.addWidget(but_html)

        but_order = QPushButton()
        but_order.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'cart.png'))
        )
        but_order.setToolTip('売買履歴（テーブル）')
        but_order.clicked.connect(self.on_order_history)
        hbox.addWidget(but_order)

    def on_contour(self):
        self.contour = contour = WinContour(self.res)
        contour.show()

    def on_explorer(self):
        self.explorer = explorer = WinExplorer(self.res, self.params)
        explorer.requestAutoSim.connect(self.on_start_autosim)
        explorer.show()

    def on_order_history(self):
        self.requestOrderHistory.emit()

    def on_order_history_html(self):
        self.requestOrderHistoryHTML.emit()

    def on_overlay(self):
        if len(self.dict_target) == 0:
            return
        self.requestOverlayAnalysis.emit(self.dict_target)

    def on_start(self):
        self.requestSimulationStart.emit(self.dict_target, self.params)

    def on_start_autosim(self, dict_target: dict, params: dict):
        self.requestAutoSimStart.emit(dict_target, params)

    def setAutoSimResult(self, result: dict):
        self.explorer.appendResult(result)

    def setInit(self, dict_target: dict):
        self.dict_target = dict_target

        self.objCode.setText(dict_target['code'])
        self.objDate.setText(dict_target['date_format'])
        self.objPriceDeltaMin.setValue(dict_target['price_delta_min'])
        self.objUnit.setValue(dict_target['unit'], False)

        self.btnStart.setEnabled(True)

    def setProgressRange(self, time_min: int, time_max: int):
        self.progress.setRange(time_min, time_max)

    def setProgressValue(self, time_current: int):
        self.progress.setValue(time_current)

    def updateProfit(self, dict_update: dict):
        self.objPricePos.setValue(dict_update['建玉価格'])
        self.objBuySell.setText(dict_update['売買'])
        self.objProfit.setValue(dict_update['含み損益'])
        self.objProfitMax.setValue(dict_update['最大含み益'])
        self.objTotal.setValue(dict_update['合計損益'])

    def updateStatus(self, state: str):
        self.objStatus.setText(state)

    def updateSystemTime(self, time_str: str):
        self.objSystemTime.setText(time_str)

    def updateTickPrice(self, time_str: str, price: float):
        # print(time_str, price)
        self.objTickTime.setText(time_str)
        self.objTickPrice.setValue(price)

    def updateTrend(self, trend: int):
        self.objTrend.setValue(trend, False)
