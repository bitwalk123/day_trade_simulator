import os

from PySide6.QtCore import (
    QMargins,
    Signal,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from structs.res import AppRes
from widgets.checks import CheckBoxLossCut
from widgets.dialog import DlgAFSetting
from widgets.buttons import EditButton, StartButton
from widgets.container import Frame, PadH
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelFlatRight,
    LabelFloat,
    LabelInt,
    LabelString,
    LabelTime,
    LabelTitle,
    LabelValue,
    LabelUnit,
)
from widgets.layouts import GridLayout


class DockMain(QDockWidget):
    requestOrderHistory = Signal()
    requestSimulationStart = Signal(dict)

    def __init__(self, res: AppRes, dict_target: dict):
        super().__init__()
        self.res = res
        self.dict_target = dict_target

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

        layout = GridLayout()
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
        objCode.setText(dict_target['code'])
        objCode.setToolTip(dict_target['name'])
        layout.addWidget(objCode, r, 1)

        r += 1
        labDate = LabelTitle('現在日付')
        layout.addWidget(labDate, r, 0)

        self.objDate = objDate = LabelDate()
        objDate.setText(dict_target['date'])
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
        objTickPriceMin.setValue(dict_target['price_tick_min'])
        layout.addWidget(objTickPriceMin, r, 1)

        unitTickPriceMin = LabelUnit('円')
        layout.addWidget(unitTickPriceMin, r, 2)

        self.objTickPriceMinEdit = objTickPriceMinEdit = EditButton(res)
        objTickPriceMinEdit.clicked.connect(self.on_modify_tick_price_min)
        layout.addWidget(objTickPriceMinEdit, r, 3)

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
        objUnit.setValue(dict_target['unit'], flag=False)
        layout.addWidget(objUnit, r, 1)

        unitUnit = LabelUnit('株')
        layout.addWidget(unitUnit, r, 2)

        self.objUnitEdit = objUnitEdit = EditButton(res)
        objUnitEdit.clicked.connect(self.on_modify_unit)
        layout.addWidget(objUnitEdit, r, 3)

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
        objTotal.setValue(0)
        layout.addWidget(objTotal, r, 1)

        unitTotal = LabelUnit('円')
        layout.addWidget(unitTotal, r, 2)

        r += 1
        labParameter = LabelFlat('【パラメータ】')
        layout.addWidget(labParameter, r, 0)

        r += 1
        labPSAR = LabelFlatRight('Parabolic SAR')
        layout.addWidget(labPSAR, r, 0)

        r += 1
        labAFinit = LabelTitle('AF（初期値）')
        layout.addWidget(labAFinit, r, 0)

        self.objAFinit = objAFinit = LabelFloat()
        objAFinit.setValue(dict_target['af_init'])
        layout.addWidget(objAFinit, r, 1, 1, 2)

        self.objAFedit = objAFedit = EditButton(res)
        objAFedit.clicked.connect(self.on_modify_af)
        layout.addWidget(objAFedit, r, 3, 3, 1)

        r += 1
        labAFstep = LabelTitle('AF（ステップ）')
        layout.addWidget(labAFstep, r, 0)

        self.objAFstep = objAFstep = LabelFloat()
        objAFstep.setValue(dict_target['af_step'])
        layout.addWidget(objAFstep, r, 1, 1, 2)

        r += 1
        labAFmax = LabelTitle('AF（最大値）')
        layout.addWidget(labAFmax, r, 0)

        self.objAFmax = objAFmax = LabelFloat()
        objAFmax.setValue(dict_target['af_max'])
        layout.addWidget(objAFmax, r, 1, 1, 2)

        r += 1
        labLossCut = LabelFlatRight('損切')
        layout.addWidget(labLossCut, r, 0)

        self.objLossCut = objLossCut = CheckBoxLossCut()
        if 'flag_losscut' in dict_target:
            objLossCut.setChecked(dict_target['flag_losscut'])
        else:
            objLossCut.setChecked(False)
        layout.addWidget(objLossCut, r, 1)

        r += 1
        labFactorLosscut = LabelTitle('損切因数')
        layout.addWidget(labFactorLosscut, r, 0)

        self.objFactorLosscut = objFactorLosscut = LabelInt()
        if 'factor_losscut' in dict_target:
            objFactorLosscut.setValue(dict_target['factor_losscut'])
        else:
            objFactorLosscut.setValue(0)
        layout.addWidget(objFactorLosscut, r, 1)

        r += 1
        base_control = QWidget()
        layout.addWidget(base_control, r, 0, 1, 4)

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(QMargins(0, 20, 0, 0))
        base_control.setLayout(vbox)

        self.btnStart = but_start = StartButton(res)
        but_start.setFixedHeight(40)
        but_start.setToolTip('シミュレーション開始')
        but_start.clicked.connect(self.on_simulation_start_request)
        vbox.addWidget(but_start)

        hbar = Frame()
        vbox.addWidget(hbar)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        hbar.setLayout(hbox)

        hpad = PadH()
        hbox.addWidget(hpad)

        but_order = QPushButton()
        but_order.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'cart.png'))
        )
        but_order.setToolTip('売買履歴（テーブル）')
        but_order.clicked.connect(self.on_order_history)
        hbox.addWidget(but_order)

    def get_losscut_param(self, dict_param: dict):
        """
        ロスカット関連パラメータ
        :param dict_param: パラメータを保持する辞書
        :return:
        """
        # 損切（ロスカット）機能が有効になっているか？
        dict_param['flag_losscut'] = self.isLossCutEnabled()
        # 損切（ロスカット）因数 ⇨ 呼び値と株数を乗じて損切価格を決める
        dict_param['factor_losscut'] = self.objFactorLosscut.getValue()

    def getAFparams(self, dict_param: dict):
        """
        Parabolic SAR の AF（加速因数）パラメータの取得
        :param dict_param: パラメータを保持する辞書
        :return:
        """
        dict_param['af_init'] = self.objAFinit.getValue()
        dict_param['af_step'] = self.objAFstep.getValue()
        dict_param['af_max'] = self.objAFmax.getValue()

    def getPriceTickMin(self) -> float:
        return self.objTickPriceMin.getValue()

    def get_tick_date_price(self, dict_param: dict):
        """
        ログデータの内、日付とティックデータの取得
        ※ 日付文字列はティックデータを matplotlib で扱う際に必ず必要になる
        :param dict_param:
        :return:
        """
        dict_param['date'] = self.dict_target['date']
        dict_param['tick'] = self.dict_target['tick']['Price']

    def isLossCutEnabled(self) -> bool:
        return self.objLossCut.isChecked()

    def on_modify_af(self):
        """
        Parabolic SAR の AF パラメータの編集ダイアログ
        :return:
        """
        dict_af = dict()
        self.getAFparams(dict_af)

        # 設定ダイアログを表示
        dlg = DlgAFSetting(self.res, dict_af)
        if dlg.exec():
            self.objAFinit.setValue(dict_af['af_init'])
            self.objAFstep.setValue(dict_af['af_step'])
            self.objAFmax.setValue(dict_af['af_max'])

    def on_modify_tick_price_min(self):
        pass

    def on_modify_unit(self):
        pass

    def on_order_history(self):
        self.requestOrderHistory.emit()

    def on_simulation_start_request(self):
        """
        シミュレーション開始リクエストの通知
        :return:
        """
        dict_param = dict()
        # シミュレータへ渡すデータ＆パラメータを準備
        self.get_losscut_param(dict_param)  # 損切パラメータ
        self.get_tick_date_price(dict_param)  # ティックデータ
        self.getAFparams(dict_param)  # PSAR パラメータ

        # 売買単位
        dict_param['unit'] = self.objUnit.getValue()
        # 呼び値
        dict_param['tick_price_min'] = self.objTickPriceMin.getValue()

        # ---------------------------------
        # 🧿 シミュレーション開始リクエストの通知
        # ---------------------------------
        self.requestSimulationStart.emit(dict_param)

    def setLossCutEnabled(self, flag: bool):
        """
        損切（ロスカット）機能を有効にするか否か設定
        :param flag: True あるいは False
        :return:
        """
        self.objLossCut.setChecked(flag)

    def setPosition(self, position: str, price: float):
        """
        建玉のポジションと価格を設定（表示）
        :param position:
        :param price:
        :return:
        """
        self.objPosition.setText(position)
        self.objPositionPrice.setValue(price)

    def setProfit(self, profit: float):
        """
        含み損益を設定（表示）
        :param profit:
        :return:
        """
        self.objProfit.setValue(profit)

    def setProfitMax(self, profit_max: float):
        """
        最大含み損益を設定（表示）
        :param profit_max: 
        :return: 
        """
        self.objProfitMax.setValue(profit_max)

    def setStatus(self, status_str: str):
        """
        タイマー状態を設定（表示）
        :param status_str:
        :return:
        """
        self.objStatus.setText(status_str)

    def setSystemTime(self, time_str: str):
        """
        システム時刻を設定（表示）
        :param time_str:
        :return:
        """
        self.objSystemTime.setText(time_str)

    def setTickPrice(self, time_str: str, price: float, trend: int):
        """
        ティック時刻と株価およびトレンドを設定（表示）
        :param time_str:
        :param price:
        :param trend:
        :return:
        """
        self.objTickTime.setText(time_str)
        self.objTickPrice.setValue(price)
        self.objTrend.setValue(trend, flag=False)

    def setTotal(self, price: float):
        """
        合計損益額を設定（表示）
        :param price:
        :return:
        """
        self.objTotal.setValue(price)
