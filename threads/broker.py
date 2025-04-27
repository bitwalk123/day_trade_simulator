import os

from PySide6.QtCore import (
    QObject,
    QThreadPool,
    Signal,
)
from PySide6.QtWidgets import QProgressBar

from structs.res import AppRes
from threads.counter import CounterLoop
from threads.preprocs import WorkerPrepDataset
from ui.dock_executor import DockExecutor
from ui.win_executor import WinExecutor
from ui.win_main import WinMain


class BrokerThreadLoop(QObject):
    errorMessage = Signal(str)
    threadFinished = Signal(bool)

    def __init__(
            self,
            res: AppRes,
            threadpool: QThreadPool,
            dock: DockExecutor,
            win: WinExecutor,
            pbar: QProgressBar
    ):
        super().__init__()
        self.res = res
        self.threadpool = threadpool
        self.dock = dock
        self.panel = win
        self.pbar = pbar

        self.winmain = None
        self.output_dir = None

        # シミュレーション対象の Excel ファイルを取得
        self.dir, self.files = dock.getExcelFiles()

        # ループカウンタ
        self.counter = CounterLoop()
        self.counter.setMaxFile(len(self.files))

        self.dict_dict_target = dict()

    def create_winmain(self, dict_target):
        self.winmain = WinMain(self.res, dict_target, self.threadpool, self.pbar)
        self.winmain.simulationCompleted.connect(self.loop_simulation)
        self.winmain.setFixedSize(1600, 800)
        self.winmain.show()

    def getDir(self) -> str:
        return self.dir

    def getFiles(self) -> list:
        return self.files

    def loop_simulation(self):
        pass

    def loop_simulation_init(self):
        file_excel = str(os.path.join(self.dir, self.files[self.cnt_file]))
        self.panel.setSrcFile(file_excel)

        prep_ds = WorkerPrepDataset(file_excel)
        prep_ds.updateProgress.connect(self.on_status_update)
        prep_ds.threadFinished.connect(self.on_excel_read_completed)
        self.threadpool.start(prep_ds)

    def loop_simulation_next(self, dict_result: dict):
        """
        name_chart = os.path.join(
            self.path_output,
            'chart_%s_%d.png' % (self.code_target, self.counter)
        )
        self.winmain.saveChart(name_chart)
        print(self.code_target, self.counter, dict_result['total'])

        """
        pass

    def start(self):
        # Excel ファイルの確認
        if self.counter.getMaxFile() == 0:
            msg = '### Excel ファイルが選択されていません。'
            self.errorMessage.emit(msg)
            self.threadFinished.emit(False)
            return

        # 出力先ディレクトリの確認
        output_dir = self.panel.getOutputDir()
        if output_dir == '':
            msg = '### 出力先ディレクトリが設定されていません。'
            self.errorMessage.emit(msg)
            self.threadFinished.emit(False)
            return
        else:
            self.output_dir = output_dir

        self.cnt_file = 0
        self.loop_simulation_init()

    def on_excel_read_completed(self, list_target):
        """
        データセットに基づき、銘柄毎のタブ画面を作成
        :param list_target:
        :return:
        """
        print('Excel read completed')

        # シミュレータウィンドウの表示
        dict_target = list_target[0]
        self.panel.setCode(dict_target['code'])
        self.panel.setDate(dict_target['date'])

        if self.winmain is None:
            self.create_winmain(dict_target)

    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)
