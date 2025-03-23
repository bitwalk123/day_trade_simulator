import os
import sys
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QProgressBar,
)

from structs.res import AppRes
from threads.preprocs import WorkerPrepDataset
from widgets.buttons import ChooseButton, FolderButton
from widgets.combo import ComboBox
from widgets.container import ScrollAreaVertical
from widgets.dialog import FileDialogExcel
from widgets.entry import EntryExcelFile
from widgets.labels import (
    LabelFlat,
    LabelFloat,
    LabelTitle,
    LabelTitleRaised,
    LabelValue,
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

        """
        self.combo_sheet = combo_sheet = ComboBox()
        toolbar.addWidget(combo_sheet)
        """

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
        labTargetCode = LabelFlat('【実験条件】')
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

        # ステータス・バー
        statusbar = StatusBar()
        self.setStatusBar(statusbar)

        self.pbar = pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        statusbar.addPermanentWidget(pbar, stretch=1)

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
        print(list_target)
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
        # self.combo_sheet.addItems(self.ent_sheet.getSheetList())
        self.but_choose.setEnabled(True)

    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
