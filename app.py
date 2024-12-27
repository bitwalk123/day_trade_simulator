#!/usr/bin/env python
# coding: utf-8
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
)


class Analyzer(QWidget):
    def __init__(self):
        super().__init__()


def main():
    app = QApplication(sys.argv)
    win = Analyzer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()