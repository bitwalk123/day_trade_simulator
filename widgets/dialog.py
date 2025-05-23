import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QMessageBox,
    QVBoxLayout,
)

from structs.res import AppRes
from widgets.container import Frame
from widgets.labels import (
    LabelFlat,
    LabelTitleLeft,
)
from widgets.spinbox import DoubleSpinBox, SpinBox


def DialogWarning(message: str):
    dlg = QMessageBox()
    dlg.setWindowTitle('警告')
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setIcon(QMessageBox.Icon.Warning)
    dlg.exec()


class DirDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setFileMode(QFileDialog.FileMode.Directory)
        self.setOption(QFileDialog.Option.ShowDirsOnly)


class FileDialogExcel(QFileDialog):
    def __init__(self, res: AppRes):
        super().__init__()
        # 初期ディレクトリを指定
        self.setDirectory(res.dir_excel)
        # 拡張子のフィルターを設定
        self.setNameFilters(
            [
                'Excel Macro (*.xlsm)',
                'All files (*)',
            ]
        )


class DlgAFSetting(QDialog):
    """
    Parabolic SAR の AF（加速因数）用の設定ダイアログ
    """

    def __init__(self, res: AppRes, dict_af: dict):
        super().__init__()
        self.dict_af = dict_af

        icon = QIcon(os.path.join(res.dir_image, 'pencil.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('AF（加速因数）の設定')

        layout_base = QVBoxLayout()
        self.setLayout(layout_base)

        base = Frame()
        layout_base.addWidget(base)

        layout = QGridLayout()
        layout.setSpacing(0)
        base.setLayout(layout)

        r = 0
        labParameter = LabelFlat('Parabolic SAR')
        layout.addWidget(labParameter, r, 0)

        r += 1
        labAFinit = LabelTitleLeft('AF（初期値）')
        layout.addWidget(labAFinit, r, 0)

        self.objAFinit = objAFinit = DoubleSpinBox()
        objAFinit.setValue(self.dict_af['af_init'])
        layout.addWidget(objAFinit, r, 1)

        r += 1
        labAFstep = LabelTitleLeft('AF（ステップ）')
        layout.addWidget(labAFstep, r, 0)

        self.objAFstep = objAFstep = DoubleSpinBox()
        objAFstep.setValue(self.dict_af['af_step'])
        layout.addWidget(objAFstep, r, 1)

        r += 1
        labAFmax = LabelTitleLeft('AF（最大値）')
        layout.addWidget(labAFmax, r, 0)

        self.objAFmax = objAFmax = DoubleSpinBox()
        objAFmax.setValue(self.dict_af['af_max'])
        layout.addWidget(objAFmax, r, 1)

        # ダイアログ用ボタンボックス
        dlgbtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        bbox = QDialogButtonBox(dlgbtn)
        bbox.accepted.connect(self.clickedAcceptButton)
        bbox.rejected.connect(self.clickedRejectButton)
        layout_base.addWidget(bbox)

    def clickedAcceptButton(self):
        """
        Ok ボタンをクリックしたときの処理
        :return:
        """
        self.dict_af['af_init'] = self.objAFinit.value()
        self.dict_af['af_step'] = self.objAFstep.value()
        self.dict_af['af_max'] = self.objAFmax.value()
        self.accept()

    def clickedRejectButton(self):
        """
        Cancel ボタンをクリックしたときの処理
        :return:
        """
        self.reject()

class DlgEntrySetting(QDialog):
    """
    Parabolic SAR の AF（加速因数）用の設定ダイアログ
    """

    def __init__(self, res: AppRes, dict_entry: dict):
        super().__init__()
        self.dict_entry = dict_entry

        icon = QIcon(os.path.join(res.dir_image, 'pencil.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('エントリ条件の設定')

        layout_base = QVBoxLayout()
        self.setLayout(layout_base)

        base = Frame()
        layout_base.addWidget(base)

        layout = QGridLayout()
        layout.setSpacing(0)
        base.setLayout(layout)

        r = 0
        labAFinit = LabelTitleLeft('EP 更新回数')
        layout.addWidget(labAFinit, r, 0)

        self.objEPupd = objEPupd = SpinBox()
        objEPupd.setValue(self.dict_entry['epupd'])
        layout.addWidget(objEPupd, r, 1)

        # ダイアログ用ボタンボックス
        dlgbtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        bbox = QDialogButtonBox(dlgbtn)
        bbox.accepted.connect(self.clickedAcceptButton)
        bbox.rejected.connect(self.clickedRejectButton)
        layout_base.addWidget(bbox)

    def clickedAcceptButton(self):
        """
        Ok ボタンをクリックしたときの処理
        :return:
        """
        self.dict_entry['epupd'] = self.objEPupd.value()
        self.accept()

    def clickedRejectButton(self):
        """
        Cancel ボタンをクリックしたときの処理
        :return:
        """
        self.reject()
