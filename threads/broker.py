import os

from PySide6.QtCore import QObject, QThreadPool, Signal

from ui.dock_executor import DockExecutor
from ui.win_executor import WinExecutor


class BrokerThreadLoop(QObject):
    errorMessage = Signal(str)
    threadFinished = Signal(bool)

    def __init__(self, dock: DockExecutor, win: WinExecutor, threadpool: QThreadPool):
        super().__init__()
        self.dock = dock
        self.win = win
        self.threadpool = threadpool
        self.output_dir = None

        self.dir, self.files = dock.getExcelFiles()
        self.counter = 0
        self.n_files = len(self.files)

    def getDir(self) -> str:
        return self.dir

    def getFiles(self) -> list:
        return self.files

    def start(self):
        # Excel ファイルの確認
        if self.n_files == 0:
            msg = '### Excel ファイルが選択されていません。'
            self.errorMessage.emit(msg)
            self.threadFinished.emit(False)
            return

        # 出力先ディレクトリの確認
        output_dir = self.win.getOutputDir()
        if output_dir == '':
            msg = '### 出力先ディレクトリが設定されていません。'
            self.errorMessage.emit(msg)
            self.threadFinished.emit(False)
            return

        self.output_dir = output_dir

        self.counter = 0
        file_excel = str(os.path.join(self.dir, self.files[self.counter]))
        self.win.setSrcFile(file_excel)
