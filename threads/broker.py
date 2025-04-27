import os

from PySide6.QtCore import (
    QObject,
    QThreadPool,
    Signal,
)
from PySide6.QtWidgets import QProgressBar

from structs.app_enum import LoopStatus
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
        self.list_target = None

        # シミュレーション対象の Excel ファイルを取得
        self.dir, self.files = dock.getExcelFiles()

        # ループカウンタ
        self.counter = CounterLoop()
        self.counter.setMaxFile(len(self.files))

        self.dict_dict_target = dict()

    def create_winmain(self, dict_target):
        if self.winmain is not None:
            self.winmain.deleteLater()
        self.winmain = WinMain(self.res, dict_target, self.threadpool, self.pbar)
        self.winmain.simulationCompleted.connect(self.loop_simulation_next)
        self.winmain.setFixedSize(1600, 800)
        self.winmain.show()

    def getDir(self) -> str:
        return self.dir

    def getFiles(self) -> list:
        return self.files

    def loop_simulation(self):
        n_condition = self.counter.getCountCondition()
        af_init = self.panel.getAFinit(n_condition)
        af_step = self.panel.getAFstep(n_condition)
        af_max = self.panel.getAFmax(n_condition)

        if self.panel.panelLossCut.IsLossCutEnabled():
            self.winmain.dock.setLossCutEnabled(True)
        else:
            self.winmain.dock.setLossCutEnabled(False)

        self.winmain.dock.objAFinit.setValue(af_init)
        self.winmain.dock.objAFstep.setValue(af_step)
        self.winmain.dock.objAFmax.setValue(af_max)
        self.winmain.autoSimulationStart()

    def loop_simulation_init(self):
        file_excel = str(os.path.join(self.dir, self.files[self.counter.getCountFile()]))
        self.panel.setSrcFile(file_excel)

        prep_ds = WorkerPrepDataset(file_excel)
        prep_ds.updateProgress.connect(self.on_status_update)
        prep_ds.threadFinished.connect(self.on_excel_read_completed)
        self.threadpool.start(prep_ds)

    def loop_simulation_next(self, dict_result: dict):
        dir_save = str(os.path.join(self.output_dir, dict_result['date']))
        if not os.path.isdir(dir_save):
            os.mkdir(dir_save)

        name_chart = 'chart_{:s}_{:0>3d}.png'.format(
            self.list_target[self.counter.getCountCode()]['code'],
            self.counter.getCountCondition()
        )
        name_chart = os.path.join(dir_save, name_chart)
        #print(name_chart)
        self.winmain.saveChart(name_chart)
        print(
            self.list_target[self.counter.getCountCode()]['code'],
            self.counter.getCountCondition(),
            dict_result['total']
        )

        # 結果の処理
        self.panel.setTotal(self.counter.getCountCondition(), dict_result['total'])

        # カウンタのインクリメント
        result = self.counter.increment()

        if result == LoopStatus.NEXT_CONDITION:
            # シミュレーション・ループ
            self.loop_simulation()
        else:
            # 全条件の Total を保存
            name_html = 'summary_{:s}_{:s}.html'.format(
                dict_result['date'],
                self.list_target[self.counter.getCountCode()]['code']
            )
            name_html = os.path.join(dir_save, name_html)
            self.panel.saveResult(name_html)

            if result == LoopStatus.NEXT_CODE:
                self.panel.clearTotal()
                dict_target = self.list_target[self.counter.getCountCode()]
                self.create_winmain(dict_target)

                # シミュレーション・ループ
                self.loop_simulation()
            elif result == LoopStatus.NEXT_FILE:
                self.loop_simulation_init()
            else:
                if self.winmain is not None:
                    self.winmain.deleteLater()
                print('complete simulation')

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

        # 水準数を設定
        self.counter.setMaxRow(self.panel.getLevelMax())

        # ループの初期設定
        self.loop_simulation_init()

    def on_excel_read_completed(self, list_target):
        """
        データセットに基づき、銘柄毎のタブ画面を作成
        :param list_target:
        :return:
        """
        print('Excel read completed')

        # ターゲット銘柄のリストを保持
        self.list_target = list_target

        # 銘柄数の設定
        self.counter.setMaxCode(len(list_target))

        # シミュレータウィンドウの表示
        dict_target = list_target[0]
        self.create_winmain(dict_target)

        # シミュレーション・ループ
        self.loop_simulation()

    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)
