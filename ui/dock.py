from PySide6.QtCore import (
    QMargins,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QDockWidget,
    QGridLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from structs.res import AppRes
from ui.dialog import DlgAFSetting
from widgets.buttons import EditButton, StartButton
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelFloat,
    LabelString,
    LabelTime,
    LabelTitle,
    LabelValue,
    LabelUnit,
)


class DockMain(QDockWidget):
    requestSimulationStart = Signal(dict)

    def __init__(self, res: AppRes, dict_target: dict):
        super().__init__()
        self.res = res
        self.dict_target = dict_target
        # self.dict_param = dict() # シミュレータへ渡すパラメータ用
        # self.dict_af = dict()  # AF（加速因数）用

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

    def get_psar_af_param(self, dict_param: dict):
        """
        Parabolic SAR の AF（加速因数）パラメータの取得
        :param dict_param:
        :return:
        """
        dict_param['af_init'] = self.objAFinit.getValue()
        dict_param['af_step'] = self.objAFstep.getValue()
        dict_param['af_max'] = self.objAFmax.getValue()

    def get_tick_date_price(self, dict_param: dict):
        """
        ログデータの内、日付とティックデータの取得
        ※ 日付文字列はティックデータを matplotlib で扱う際に必ず必要になる
        :param dict_param:
        :return:
        """
        dict_param['date'] = self.dict_target['date']
        dict_param['tick'] = self.dict_target['tick']['Price']

    def on_modify_af(self):
        """
        Parabolic SAR の AF パラメータの編集ダイアログ
        :return:
        """
        dict_af = dict()
        self.get_psar_af_param(dict_af)

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

    def on_simulation_start_request(self):
        dict_param = dict()
        # シミュレータへ渡すデータ＆パラメータを準備
        self.get_tick_date_price(dict_param)
        self.get_psar_af_param(dict_param)
        # 売買単位
        dict_param['unit'] = self.objUnit.getValue()

        # -----------------------------
        # 🔆 シミュレーション開始のリクエスト
        # -----------------------------
        self.requestSimulationStart.emit(dict_param)

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
