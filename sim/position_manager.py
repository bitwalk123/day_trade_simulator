import pandas as pd


class PositionManager:
    """
    建玉管理クラス
    """

    def __init__(self, unit):
        self.unit = unit
        self.trend = 0
        self.price = 0
        self.total = 0
        self.order = 0

        dict_columns = {
            'Order': [],
            'Datetime': [],
            'Position': [],
            'Price': [],
            'Profit': [],
            'Note': [],
        }
        df = pd.DataFrame.from_dict(dict_columns)
        self.df_order = df.astype(object)

        dict_columns = {
            'Datetime': [],
            'Price': [],
            'Profit': [],
            'Order': [],
        }
        df = pd.DataFrame.from_dict(dict_columns)
        self.df_profit = df.astype(object)

    def open(self, t, price, note=''):
        self.price = price

        if self.trend > 0:
            msg = '買建'
        elif self.trend < 0:
            msg = '売建'
        else:
            msg = '不明'

        self.order += 1
        r = len(self.df_order)
        self.df_order.at[r, 'Order'] = self.order
        self.df_order.at[r, 'Datetime'] = t
        self.df_order.at[r, 'Position'] = msg
        self.df_order.at[r, 'Price'] = self.price
        self.df_order.at[r, 'Note'] = note

    def close(self, t, price, note=''):
        if self.trend > 0:
            msg = '売埋'
            profit = (price - self.price) * self.unit
        elif self.trend < 0:
            msg = '買埋'
            profit = (self.price - price) * self.unit
        else:
            msg = '不明'
            profit = 0

        r = len(self.df_order)
        self.df_order.at[r, 'Order'] = self.order
        self.df_order.at[r, 'Datetime'] = t
        self.df_order.at[r, 'Position'] = msg
        self.df_order.at[r, 'Price'] = price
        self.df_order.at[r, 'Profit'] = profit
        self.df_order.at[r, 'Note'] = note

        self.price = 0
        self.total += profit

    def has_position(self):
        if self.price > 0:
            return True
        else:
            return False

    def set_trend(self, trend):
        self.trend = trend

    def get_trend(self):
        return self.trend

    def get_total(self):
        return int(self.total)

    def get_order_history(self):
        return self.df_order

    def eval_profit(self, t, price):
        if not self.has_position():
            return

        if self.trend > 0:
            profit = (price - self.price) * self.unit
        elif self.trend < 0:
            profit = (self.price - price) * self.unit
        else:
            return

        r = len(self.df_profit)
        self.df_profit.at[r, 'Datetime'] = t
        self.df_profit.at[r, 'Price'] = price
        self.df_profit.at[r, 'Profit'] = profit
        self.df_profit.at[r, 'Order'] = self.order

    def get_profit_history(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                'Profit': self.df_profit['Profit'].astype(float).values,
                'Order': self.df_profit['Order'].astype(int).values,
            },
            index=pd.to_datetime(self.df_profit['Datetime'])
        )
