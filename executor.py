import os
import sys
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QProgressBar,
    QSizePolicy,
    QWidget,
)

from structs.res import AppRes
from threads.preprocs import WorkerPrepDataset
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
from widgets.entry import EntryDir, EntryExcelFile
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelFloat,
    LabelTitle,
    LabelTitleRaised,
    LabelValue,
)
from widgets.layouts import GridLayout, HBoxLayout
from widgets.statusbar import StatusBar
from widgets.toolbar import ToolBar


class Executor(QMainWindow):
    __app_name__ = 'Executor'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()
        self.dict_dict_target = dict()

        self.code_target = None
        self.winmain: None | WinMain = None

        # ループ用カウンタ
        self.counter: int = 0
        self.counter_max: int = 0

        # ウィンドウ・アイコンとタイトル
        icon = QIcon(os.path.join(res.dir_image, 'start.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)

        # =====================================================================
        #  UI
        # =====================================================================
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

        sa = ScrollAreaVertical()
        self.setCentralWidget(sa)

        base = QWidget()
        sa.setWidget(base)

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
        if self.winmain is not None:
            self.winmain.deleteLater()
        event.accept()  # let the window close

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
            path = os.path.join(basedir, dateStr)
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
        self.code_target = self.comboCode.currentText()
        self.counter_max = self.panelParam.getLevelMax()
        self.counter = 0
        self.loop_simulation()

    def loop_simulation(self):
        dict_target = self.dict_dict_target[self.code_target]

        if self.winmain is not None:
            self.winmain.hide()
            self.winmain.deleteLater()
        # ---------------
        #  Simulator 起動
        # ---------------
        self.winmain = WinMain(self.res, dict_target, self.threadpool, self.pbar)
        self.winmain.simulationCompleted.connect(self.next_simulation)
        self.winmain.setFixedSize(1600, 800)
        self.winmain.show()
        self.winmain.autoSimulationStart()
        # カウンターのインクリメント
        self.counter += 1

    def next_simulation(self, dict_result: dict):
        print(dict_result['total'])
        if self.counter < self.counter_max:
            self.loop_simulation()
        else:
            print('Completed!')

    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
