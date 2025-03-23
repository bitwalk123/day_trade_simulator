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
        self.winmain: None | WinMain = None

        icon = QIcon(os.path.join(res.dir_image, 'start.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)

        toolbar = ToolBar()
        self.addToolBar(toolbar)

        but_folder = FolderButton(res)
        but_folder.clicked.connect(self.on_file_dialog_open)
        toolbar.addWidget(but_folder)

        self.ent_sheet = ent_sheet = EntryExcelFile()
        ent_sheet.setFixedWidth(200)
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

        r += 1
        labDate = LabelTitle('現在日付')
        layout.addWidget(labDate, r, 0)

        self.objDate = objDate = LabelDate()
        layout.addWidget(objDate, r, 1)

        r += 1
        labTargetCode = LabelFlat('【水準】')
        layout.addWidget(labTargetCode, r, 0)

        r += 1
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

            self.af_init.append(objAFinit)
            self.af_step.append(objAFstep)
            self.af_max.append(objAFmax)
            self.total.append(objTotal)

        r += 1
        base_output = QWidget()
        base_output.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )
        layout.addWidget(base_output, r, 0, 1, 5)

        layout_output = HBoxLayout()
        base_output.setLayout(layout_output)

        labOutput = LabelTitle('出力先')
        layout_output.addWidget(labOutput)

        self.entOutput = entOutput = EntryDir()
        layout_output.addWidget(entOutput)

        but_dir = FolderButton(res)
        but_dir.clicked.connect(self.on_dir_dialog_select)
        layout_output.addWidget(but_dir)

        padh = PadH()
        layout_output.addWidget(padh)

        # ステータス・バー
        statusbar = StatusBar()
        self.setStatusBar(statusbar)

        self.pbar = pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        statusbar.addPermanentWidget(pbar, stretch=1)

        r += 1
        self.btnStart = but_start = StartButton(res)
        but_start.setFixedHeight(40)
        but_start.setToolTip('シミュレーション開始')
        but_start.clicked.connect(self.on_simulation_start)
        layout.addWidget(but_start, r, 0, 1, 5)

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

        """
        # 現在のタブをすべて削除
        self.base.deleteAllTabs()
        # 新しいタブを追加
        for dict_target in list_target:
            code = dict_target['code']
            tabobj = WinMain(self.res, dict_target, self.threadpool, self.pbar)
            self.base.addTab(tabobj, code)
        """
        # 進捗をリセット
        self.pbar.reset()

    def on_dir_dialog_select(self):
        dialog = DirDialog()
        if not dialog.exec():
            return

        basedir = dialog.selectedFiles()[0]
        dateStr = self.objDate.text()
        if dateStr is not None:
            self.entOutput.setText(os.path.join(basedir, dateStr))

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
        code = self.comboCode.currentText()
        dict_target = self.dict_dict_target[code]
        if self.winmain is None:
            self.winmain = WinMain(self.res, dict_target, self.threadpool, self.pbar)
        self.winmain.show()

    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
