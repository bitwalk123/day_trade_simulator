from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSizePolicy

from structs.res import AppRes
from widgets.buttons import FolderButton
from widgets.container import Widget, PadH
from widgets.entry import EntryDir
from widgets.labels import LabelTitle
from widgets.layouts import HBoxLayout


class PanelOutput(Widget):
    selectDir = Signal()

    def __init__(self, res: AppRes):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        layout_output = HBoxLayout()
        self.setLayout(layout_output)

        labOutput = LabelTitle('出力先')
        layout_output.addWidget(labOutput)

        self.entOutput = entOutput = EntryDir()
        layout_output.addWidget(entOutput)

        but_dir = FolderButton(res)
        but_dir.clicked.connect(self.on_dir_dialog_select)
        layout_output.addWidget(but_dir)

        padh = PadH()
        layout_output.addWidget(padh)

    def on_dir_dialog_select(self):
        """
        dialog = DirDialog()
        if not dialog.exec():
            return

        basedir = dialog.selectedFiles()[0]
        dateStr = self.objDate.text()
        if dateStr is not None:
            self.entOutput.setText(os.path.join(basedir, dateStr))
        """
        self.selectDir.emit()

    def setOutput(self, path: str):
        self.entOutput.setText(path)
