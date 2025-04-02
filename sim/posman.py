import pandas as pd


class PositionManager:
    """
    建玉管理クラス
    """
    __version__ = '1.0.1'

    def __init__(self, unit: int = 100):
        # インスタンス変数の初期化
        self.unit = unit  # 売買単位
        self.trend: int = 0  # Parabolic SAR トレンドシグナル
        self.price = 0  # 建玉取得時の株価
        self.profit_max = 0  # 最大含み益
        self.total = 0  # 損益合計
        self.order = 0  # 注文番号

        # 注文履歴用データフレーム
        dict_columns = {
            'Order': [],  # int
            'Datetime': [],  # ts
            'Position': [],  # str
            'Price': [],  # int
            'Profit': [],  # int
            'ProfitMax': [],  # int
            'Note': [],  # str
        }
        df = pd.DataFrame.from_dict(dict_columns)
        self.df_order = df.astype(object)
        # 出力用関数に渡す列フォーマット識別子
        self.column_format = ['int', 'ts', 'str', 'int', 'int', 'int', 'str']
        # 出力用関数に渡す列名
        self.column_name = ['#', '注文時刻', '建玉', '株価', '損益', '最大含み益', '備　　考']

        # 含み損益用データフレーム（プロット用）
        dict_columns = {
            'Datetime': [],
            'Price': [],
            'Profit': [],
            'ProfitMax': [],
            'Order': [],
        }
        df = pd.DataFrame.from_dict(dict_columns)
        self.df_profit = df.astype(object)

    def evalProfit(self, t: pd.Timestamp, price: float) -> dict:
        """
        含み損益を評価
        :param t:
        :param price:
        :return:
        """
        profit = self.get_profit(price)
        if self.profit_max < profit:
            self.profit_max = profit

        r = len(self.df_profit)
        self.df_profit.at[r, 'Datetime'] = t
        self.df_profit.at[r, 'Price'] = price
        self.df_profit.at[r, 'Profit'] = profit
        self.df_profit.at[r, 'ProfitMax'] = self.profit_max
        self.df_profit.at[r, 'Order'] = self.order

        dict_profit = dict()
        dict_profit['profit'] = profit
        dict_profit['profit_max'] = self.profit_max

        return dict_profit

    def hasPosition(self):
        """
        建玉を持っているか？
        :return:
        """
        if self.price > 0:
            return True
        else:
            return False

    def get_profit(self, price: float):
        if not self.hasPosition():
            return 0.

        if self.trend > 0:
            return (price - self.price) * self.unit
        elif self.trend < 0:
            return (self.price - price) * self.unit
        else:
            return 0,

    def getColFormatOrder(self) -> list:
        """
        注文履歴のデータフレームの列書式
        :return:
        """
        return self.column_format

    def getOrderHistory(self) -> pd.DataFrame:
        """
        注文履歴を返す
        :return:
        """
        df: pd.DataFrame = self.df_order.copy()
        df.columns = self.column_name
        return df

    def getProfitHistory(self) -> pd.DataFrame:
        """
        含み損益を返す
        :return:
        """
        return pd.DataFrame(
            {
                'Profit': self.df_profit['Profit'].astype(float).values,
                'ProfitMax': self.df_profit['ProfitMax'].astype(float).values,
                'Order': self.df_profit['Order'].astype(int).values,
            },
            index=pd.to_datetime(self.df_profit['Datetime'])
        )

    def getTotal(self) -> float:
        """
        保持している実現損益を返す
        :return:
        """
        return self.total

    def getTrend(self):
        """
        保持している PSAR トレンドを返す
        :return:
        """
        return self.trend

    def posClose(self, t: pd.Timestamp, price: float, note: str = '') -> float:
        """
        建玉の返却
        :param t:
        :param price:
        :param note:
        :return:
        """
        # トレンドに従って建玉返済が「売埋」か「買埋」を識別
        if self.trend > 0:
            msg = '売埋'
            profit = (price - self.price) * self.unit
        elif self.trend < 0:
            msg = '買埋'
            profit = (self.price - price) * self.unit
        else:
            msg = '不明'
            profit = 0

        # 注文履歴に売買イベントを追加
        r = len(self.df_order)
        self.df_order.at[r, 'Order'] = self.order
        self.df_order.at[r, 'Datetime'] = t
        self.df_order.at[r, 'Position'] = msg
        self.df_order.at[r, 'Price'] = price
        self.df_order.at[r, 'Profit'] = profit
        self.df_order.at[r, 'ProfitMax'] = self.profit_max
        self.df_order.at[r, 'Note'] = note

        # 建玉情報をリセット
        self.price = 0
        self.profit_max = 0

        # 損益合計を更新
        self.total += profit

        # 売買情報を返す（アプリ画面表示用）
        return self.total

    def posOpen(self, t: pd.Timestamp, price: float, note: str = '') -> dict:
        """
        建玉の取得
        :param t: 時刻
        :param price: 株価
        :param note: 備考文字列
        :return:
        """
        # 建玉取得時の株価を保持
        self.price = price

        # トレンドに従って「買建」か「売建」か識別
        if self.trend > 0:
            msg = '買建'
        elif self.trend < 0:
            msg = '売建'
        else:
            msg = '不明'

        # 注文履歴に売買イベントを追加
        self.order += 1  # 注文番号のインクリメント
        r = len(self.df_order)
        self.df_order.at[r, 'Order'] = self.order
        self.df_order.at[r, 'Datetime'] = t
        self.df_order.at[r, 'Position'] = msg
        self.df_order.at[r, 'Price'] = self.price
        self.df_order.at[r, 'Note'] = note

        # 売買情報を返す（アプリ画面表示用）
        dict_position = dict()
        dict_position['position'] = msg
        dict_position['price'] = price
        return dict_position

    def setTrend(self, trend: int):
        """
        PSAR トレンドの設定
        :param trend:
        :return:
        """
        self.trend = trend
