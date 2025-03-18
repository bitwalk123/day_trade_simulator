from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)
import pandas as pd
import yfinance as yf


class PrepDatasetSignal(QObject):
    threadFinished = Signal(list)
    updateProgress = Signal(int)


class WorkerPrepDataset(QRunnable, PrepDatasetSignal):
    def __init__(self, file_excel: str):
        super().__init__()
        self.file_excel = file_excel

    def run(self):
        list_target = list()

        # ワークシート Cover の読み込み
        name_sheet_cover = 'Cover'
        df_cover = pd.read_excel(
            self.file_excel,
            sheet_name=name_sheet_cover,
            header=None,
            index_col=0,
        )

        # ワークシート Cover の列数
        n = len(df_cover.columns)
        # 銘柄毎にループ
        for c in range(n):
            dict_target = dict()

            # 銘柄コード
            r = list(df_cover.index).index('銘柄コード')
            code = df_cover.iloc[r, c]
            dict_target['code'] = code

            # Yahoo Finance から会社名を取得
            symbol = '%s.T' % code
            ticker = yf.Ticker(symbol)
            name = ticker.info['longName']
            dict_target['name'] = name

            # 現在日付の保持
            r = list(df_cover.index).index('現在日付')
            date = df_cover.iloc[r, c].replace('/', '-')
            dict_target['date'] = date

            # 呼び値
            r = list(df_cover.index).index('呼値')
            price_tick_min = df_cover.iloc[r, c]
            dict_target['price_tick_min'] = price_tick_min

            # AF
            r = list(df_cover.index).index('AF（初期値）')
            af_init = df_cover.iloc[r, c]
            dict_target['af_init'] = af_init

            r = list(df_cover.index).index('AF（ステップ）')
            af_step = df_cover.iloc[r, c]
            dict_target['af_step'] = af_step

            r = list(df_cover.index).index('AF（最大値）')
            af_max = df_cover.iloc[r, c]
            dict_target['af_max'] = af_max

            # 銘柄コードから、ティックデータ用ワークシート名を特定しティックデータを読み込む
            name_sheet_tick = 'tick_%s' % code
            df_tick = pd.read_excel(
                self.file_excel,
                sheet_name=name_sheet_tick,
                header=0,
            )
            # 時刻データを日付を含んだ Matplotlib で扱える形式に変換、インデックスへ
            df_tick.index = [pd.to_datetime('%s %s' % (date, t)) for t in df_tick['Time']]
            df_tick.index.name = 'Datetime'
            df_tick = df_tick[['Price', 'TREND', 'EP', 'AF', 'PSAR']]
            dict_target['tick'] = df_tick

            list_target.append(dict_target)

        self.threadFinished.emit(list_target)
