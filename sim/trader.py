import numpy as np
import pandas as pd


class Trader():
    def __init__(self, unit: int):
        self.unit = unit

        self.id_order = 1
        self.loss_max = 0
        self.position = '無し'
        self.price = 0
        self.profit_max = 0
        self.total = 0
        self.trend_psar = 0

        self.l_order = '#'
        self.l_time = '時　刻'
        self.l_buysell = '売　買'
        self.l_price = '金　額'
        self.l_profit = '損　益'
        self.l_profit_max = '最大益'
        self.l_loss_max = '最大損'
        self.l_note = '備　考'

        self.dict_columns = {
            self.l_order: [],
            self.l_time: [],
            self.l_buysell: [],
            self.l_price: [],
            self.l_profit: [],
            self.l_profit_max: [],
            self.l_loss_max: [],
            self.l_note: [],
        }
        # カラムのフォーマット
        self.list_format = ['int', 'ts', 'str', 'int', 'int', 'int', 'int', 'str']

        # 注文履歴
        df = pd.DataFrame.from_dict(self.dict_columns)
        self.df_order = df.astype(str)

    def closePosition(self, t_current, p_current, transaction, note=''):
        profit = self.getProfit(p_current)
        self.total += profit

        if self.position == '買建':
            action = '売埋'
        elif self.position == '売建':
            action = '買埋'
        else:
            action = '不明'

        transaction[self.l_order] = self.id_order
        transaction[self.l_time] = t_current
        transaction[self.l_buysell] = action
        transaction[self.l_price] = p_current * self.unit
        transaction[self.l_profit] = profit
        transaction[self.l_profit_max] = self.profit_max
        transaction[self.l_loss_max] = self.loss_max
        transaction[self.l_note] = note
        self.updateOrderHistory(transaction)

        self.price = 0
        self.profit_max = 0
        self.loss_max = 0
        self.position = '無し'

        self.id_order += 1

    def openPosition(self, t_current, p_current, transaction, note=''):
        self.price = p_current

        if self.trend_psar > 0:
            self.position = '買建'
        elif self.trend_psar < 0:
            self.position = '売建'
        else:
            self.position = '不明'
            self.price = 0

        transaction[self.l_order] = self.id_order
        transaction[self.l_time] = t_current
        transaction[self.l_buysell] = self.position
        transaction[self.l_price] = self.price * self.unit
        transaction[self.l_profit] = ''
        transaction[self.l_profit_max] = ''
        transaction[self.l_loss_max] = ''
        transaction[self.l_note] = note
        self.updateOrderHistory(transaction)

    def getLossMax(self):
        return self.loss_max

    def getPosition(self):
        return self.position

    def getPrice(self):
        # 建玉取得価格
        return self.price

    def getProfit(self, p_current):
        if self.position == '買建':
            s = 1
        elif self.position == '売建':
            s = -1
        else:
            s = 0

        profit = (p_current - self.price) * self.unit * s

        if profit > self.profit_max:
            self.profit_max = profit
        if profit < self.loss_max:
            self.loss_max = profit

        return profit

    def getProfitMax(self):
        return self.profit_max

    def getTrend(self):
        return self.trend_psar

    def getTotal(self):
        return self.total

    def getUnit(self):
        return self.unit

    def hasPosition(self):
        if self.price > 0:
            return True
        else:
            return False

    def setTrend(self, trend):
        self.trend_psar = trend

    def updateOrderHistory(self, transaction: dict):
        r = len(self.df_order)
        for key in transaction.keys():
            self.df_order.at[r, key] = transaction[key]

    def getOrderHistory(self):
        return self.df_order

    def getColumnFormat(self):
        return self.list_format

    def calcProfitTotal(self):
        r = len(self.df_order)
        total = 0
        for i in range(r):
            value = self.df_order.at[i, self.l_profit]
            if type(value) is not str:
                total = total + value

        self.df_order.at[r, self.l_order] = ''
        self.df_order.at[r, self.l_time] = ''
        self.df_order.at[r, self.l_buysell] = ''
        self.df_order.at[r, self.l_price] = '損益合計'
        self.df_order.at[r, self.l_profit] = total
        self.df_order.at[r, self.l_profit_max] = ''
        self.df_order.at[r, self.l_loss_max] = ''
        self.df_order.at[r, self.l_note] = ''

    def getColumnFormat4HTML(self):
        formatters = {
            self.l_order: lambda x: '{:*>3}'.format(x),
        }
