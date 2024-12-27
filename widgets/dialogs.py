from PySide6.QtWidgets import QMessageBox


def DialogWarning(message: str):
    dlg = QMessageBox()
    dlg.setWindowTitle('警告')
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setIcon(QMessageBox.Icon.Warning)
    dlg.exec()
