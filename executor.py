import os
import sys
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QProgressBar,
    QWidget,
)

from structs.res import AppRes
from threads.preprocs import WorkerPrepDataset
from ui.panel_losscut import PanelLossCut
from ui.panel_output import PanelOutput
from ui.panel_param import PanelParam
from ui.win_main import WinMain
from widgets.buttons import (
    ChooseButton,
    FolderButton,
    StartButton,
)
from widgets.combo import ComboBox
from widgets.container import PadH, ScrollAreaVertical
from widgets.dialog import DirDialog, FileDialogExcel
from widgets.entry import EntryExcelFile
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelTitle,
)
from widgets.layouts import GridLayout
from widgets.statusbar import StatusBar
from widgets.toolbar import ToolBar


class Executor(QMainWindow):
    __app_name__ = 'Executor'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()
        self.dict_dict_target = dict()

        # シミュレーション・ループ用オブジェクト＆カウンタ
        self.code_target = None
        self.winmain: None | WinMain = None
        self.counter: int = 0
        self.counter_max: int = 0
        self.path_output = None

        # ウィンドウ・アイコンとタイトル
        icon = QIcon(os.path.join(res.dir_image, 'start.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)

        # =====================================================================
        #  UI
        # =====================================================================
        # ツールバー
        toolbar = ToolBar()
        self.addToolBar(toolbar)

        but_folder = FolderButton(res)
        but_folder.clicked.connect(self.on_file_dialog_open)
        toolbar.addWidget(but_folder)

        self.ent_sheet = ent_sheet = EntryExcelFile()
        toolbar.addWidget(ent_sheet)

        self.but_choose = but_choose = ChooseButton(res)
        but_choose.setDisabled(True)
        but_choose.clicked.connect(self.on_file_selected)
        toolbar.addWidget(but_choose)

        """
        but_test = QToolButton()
        but_test.setText('テスト')
        but_test.clicked.connect(self.function_test)
        toolbar.addWidget(but_test)
        """

        # メイン
        base = QWidget()
        self.setCentralWidget(base)

        layout = GridLayout()
        base.setLayout(layout)

        r = 0
        labCode = LabelTitle('銘柄コード')
        layout.addWidget(labCode, r, 0)

        self.comboCode = comboCode = ComboBox()
        layout.addWidget(comboCode, r, 1)

        hpad = PadH()
        layout.addWidget(hpad, r, 2)

        r += 1
        labDate = LabelTitle('現在日付')
        layout.addWidget(labDate, r, 0)

        self.objDate = objDate = LabelDate()
        layout.addWidget(objDate, r, 1)

        r += 1
        labLossCut = LabelTitle('ロスカット')
        layout.addWidget(labLossCut, r, 0)

        self.panelLossCut = panel_losscut = PanelLossCut(res)
        layout.addWidget(panel_losscut, r, 1, 1, 2)

        r += 1
        labTargetCode = LabelFlat('【水準】')
        layout.addWidget(labTargetCode, r, 0)

        r += 1
        self.panelParam = panel_param = PanelParam(res)
        layout.addWidget(panel_param, r, 0, 1, 3)

        r += 1
        self.panelOutput = panel_output = PanelOutput(res)
        panel_output.selectDir.connect(self.on_dir_dialog_select)
        layout.addWidget(panel_output, r, 0, 1, 3)

        r += 1
        self.btnStart = but_start = StartButton(res)
        but_start.setFixedHeight(40)
        but_start.setToolTip('シミュレーション開始')
        but_start.clicked.connect(self.on_simulation_start)
        layout.addWidget(but_start, r, 0, 1, 3)

        # ステータス・バー
        statusbar = StatusBar()
        self.setStatusBar(statusbar)

        self.pbar = pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        statusbar.addPermanentWidget(pbar, stretch=1)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        self.delete_winmain()
        event.accept()  # let the window close

    def delete_winmain(self):
        if self.winmain is not None:
            self.winmain.hide()
            self.winmain.deleteLater()
            self.winmain = None

    def on_file_selected(self):
        """
        選択した Excel ファイルの読み込みと解析用データ準備
        :param file_excel:
        :return:
        """
        file_excel = self.ent_sheet.get_ExcelFile()
        prep_ds = WorkerPrepDataset(file_excel)
        prep_ds.updateProgress.connect(self.on_status_update)
        prep_ds.threadFinished.connect(self.on_dataset_ready)
        self.threadpool.start(prep_ds)

    def on_dataset_ready(self, list_target):
        """
        データセットに基づき、銘柄毎のタブ画面を作成
        :param list_target:
        :return:
        """
        for dict_target in list_target:
            code = dict_target['code']
            self.comboCode.addItem(code)
            self.dict_dict_target[code] = dict_target

        self.objDate.setText(list_target[0]['date'])

        # 進捗をリセット
        self.pbar.reset()

    def on_dir_dialog_select(self):
        dialog = DirDialog()
        if not dialog.exec():
            return

        basedir = dialog.selectedFiles()[0]
        dateStr = self.objDate.text()
        if dateStr is not None:
            self.path_output = path = os.path.join(basedir, dateStr)
            self.panelOutput.setOutput(path)

    def on_file_dialog_open(self):
        """
        Excel Macro ファイルの読み込み
        :return:
        """
        dialog = FileDialogExcel(self.res)
        # ファイルを選択されなければ何もしない
        if not dialog.exec():
            return

        file_excel = dialog.selectedFiles()[0]
        self.ent_sheet.setExcelFile(file_excel)
        self.but_choose.setEnabled(True)

    def on_simulation_start(self):
        if self.path_output is None:
            print('結果の出力先が指定されていないので開始できません。')
            return
        elif not os.path.isdir(self.path_output):
            os.mkdir(self.path_output)

        self.panelParam.clearTotal()
        self.code_target = self.comboCode.currentText()
        self.counter_max = self.panelParam.getLevelMax()
        self.counter = 0

        # シミュレーション・ループ開始
        self.loop_simulation()

    def loop_simulation(self):
        # カウンターのインクリメント
        self.counter += 1

        # ---------------
        #  Simulator 起動
        # ---------------
        if self.winmain == None:
            dict_target = self.dict_dict_target[self.code_target]

            dict_target['flag_losscut'] = False
            dict_target['af_init'] = self.panelParam.getAFinit(self.counter)
            dict_target['af_step'] = self.panelParam.getAFstep(self.counter)
            dict_target['af_max'] = self.panelParam.getAFmax(self.counter)

            if self.panelLossCut.IsLossCutEnabled():
                dict_target['flag_losscut'] = True
                dict_target['factor_losscut']=self.panelLossCut.getLossCutFactor()
            else:
                dict_target['flag_losscut'] = False

            self.winmain = WinMain(self.res, dict_target, self.threadpool, self.pbar)
            self.winmain.simulationCompleted.connect(self.next_simulation)
            self.winmain.setFixedSize(1600, 800)
            self.winmain.show()
        else:
            af_init = self.panelParam.getAFinit(self.counter)
            af_step = self.panelParam.getAFstep(self.counter)
            af_max = self.panelParam.getAFmax(self.counter)

            if self.panelLossCut.IsLossCutEnabled():
                self.winmain.dock.setLossCutEnabled(True)
            else:
                self.winmain.dock.setLossCutEnabled(False)

            self.winmain.dock.objAFinit.setValue(af_init)
            self.winmain.dock.objAFstep.setValue(af_step)
            self.winmain.dock.objAFmax.setValue(af_max)

        self.winmain.autoSimulationStart()

    def next_simulation(self, dict_result: dict):
        name_chart = os.path.join(
            self.path_output,
            'chart_%s_%d.png' % (self.code_target, self.counter)
        )
        self.winmain.saveChart(name_chart)
        print(self.code_target, self.counter, dict_result['total'])

        # 結果の処理
        self.panelParam.setTotal(self.counter, dict_result['total'])

        # ループまたは終了処理
        if self.counter < self.counter_max:
            self.loop_simulation()
        else:
            self.delete_winmain()
            name_html = os.path.join(
                self.path_output,
                'summary_%s_%d.html' % (self.code_target, self.counter)
            )
            self.panelParam.getResult(name_html)
            print('Completed!')

    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)

    def function_test(self):
        self.panelParam.getResult('test.html')


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
