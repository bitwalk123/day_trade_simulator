import sys

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget

from structs.res import AppRes
from widgets.buttons import FolderButton, StartButton
from widgets.container import ScrollAreaVertical
from widgets.entry import Entry
from widgets.layouts import GridLayout


class Designer(QMainWindow):
    __app_name__ = 'Experiment Designer'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()

        sa = ScrollAreaVertical()
        self.setCentralWidget(sa)

        base = QWidget()
        sa.setWidget(base)

        layout = GridLayout()
        base.setLayout(layout)

        r = 0
        but_folder = FolderButton(res)
        layout.addWidget(but_folder, r, 0)

        ent_folder = Entry()
        ent_folder.setFixedWidth(200)
        layout.addWidget(ent_folder, r, 1)

        but_folder = StartButton(res)
        layout.addWidget(but_folder, r, 2)

def main():
    app = QApplication(sys.argv)
    win = Designer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
