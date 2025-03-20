import pandas as pd


class PositionManager:
    """
    建玉管理クラス
    """

    def __init__(self, unit: int):
        self.unit = unit
        self.trend = 0
        self.price = 0
        self.profit_max = 0  # 最大含み益
        self.total = 0
        self.order = 0  # 注文番号

        # 注文履歴
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
        self.column_format = ['int', 'ts', 'str', 'int', 'int', 'int', 'str']
        self.column_name = ['#', '注文時刻', '建玉', '株価', '損益', '最大含み益', '備　　考']

        # 含み損益
        dict_columns = {
            'Datetime': [],
            'Price': [],
            'Profit': [],
            'ProfitMax': [],
            'Order': [],
        }
        df = pd.DataFrame.from_dict(dict_columns)
        self.df_profit = df.astype(object)

    def open(self, t, price, note='') -> dict:
        """
        建玉の取得
        :param t:
        :param price:
        :param note:
        :return:
        """
        self.price = price

        if self.trend > 0:
            msg = '買建'
        elif self.trend < 0:
            msg = '売建'
        else:
            msg = '不明'

        # 注文履歴
        self.order += 1  # 注文番号のインクリメント
        r = len(self.df_order)
        self.df_order.at[r, 'Order'] = self.order
        self.df_order.at[r, 'Datetime'] = t
        self.df_order.at[r, 'Position'] = msg
        self.df_order.at[r, 'Price'] = self.price
        self.df_order.at[r, 'Note'] = note

        dict_position = dict()
        dict_position['position'] = msg
        dict_position['price'] = price
        return dict_position

    def close(self, t, price, note='') -> float:
        """
        建玉の返却
        :param t:
        :param price:
        :param note:
        :return:
        """
        if self.trend > 0:
            msg = '売埋'
            profit = (price - self.price) * self.unit
        elif self.trend < 0:
            msg = '買埋'
            profit = (self.price - price) * self.unit
        else:
            msg = '不明'
            profit = 0

        # 注文履歴
        r = len(self.df_order)
        self.df_order.at[r, 'Order'] = self.order
        self.df_order.at[r, 'Datetime'] = t
        self.df_order.at[r, 'Position'] = msg
        self.df_order.at[r, 'Price'] = price
        self.df_order.at[r, 'Profit'] = profit
        self.df_order.at[r, 'ProfitMax'] = self.profit_max
        self.df_order.at[r, 'Note'] = note

        self.price = 0
        self.profit_max = 0
        self.total += profit

        return self.total

    def has_position(self):
        """
        建玉を持っているか？
        :return:
        """
        if self.price > 0:
            return True
        else:
            return False

    def set_trend(self, trend):
        """
        PSAR トレンドの設定
        :param trend:
        :return:
        """
        self.trend = trend

    def get_column_format_order(self) -> list:
        """
        注文履歴のデータフレームの列書式
        :return:
        """
        return self.column_format

    def get_trend(self):
        """
        保持している PSAR トレンドを返す
        :return:
        """
        return self.trend

    def get_total(self) -> float:
        """
        保持している実現損益を返す
        :return:
        """
        return self.total

    def get_order_history(self) -> pd.DataFrame:
        """
        注文履歴を返す
        :return:
        """
        df: pd.DataFrame = self.df_order.copy()
        df.columns = self.column_name
        return df

    def eval_profit(self, t, price) -> dict:
        """
        含み損益を評価
        :param t:
        :param price:
        :return:
        """
        profit = self.get_profit(t, price)
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

    def get_profit(self, t, price):
        if not self.has_position():
            return 0.

        if self.trend > 0:
            return (price - self.price) * self.unit
        elif self.trend < 0:
            return (self.price - price) * self.unit
        else:
            return 0,

    def get_profit_history(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                'Profit': self.df_profit['Profit'].astype(float).values,
                'ProfitMax': self.df_profit['ProfitMax'].astype(float).values,
                'Order': self.df_profit['Order'].astype(int).values,
            },
            index=pd.to_datetime(self.df_profit['Datetime'])
        )
