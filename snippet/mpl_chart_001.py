import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from PySide6.QtWidgets import QApplication, QMainWindow


class Canvas(FigureCanvas):
    def __init__(self):
        self.fig = fig = Figure()
        super().__init__(fig)
        plt.rcParams["figure.titlesize"] = 'x-large'

        self.ax = ax = fig.add_subplot(111)
        fig.suptitle('suptitle')
        ax.set_title('title', fontsize='small')

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        canvas = Canvas()
        self.setCentralWidget(canvas)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
