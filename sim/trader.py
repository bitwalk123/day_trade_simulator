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

    def closePosition(self, t_current, p_current, transaction, note=''):
        profit = self.getProfit(p_current)
        self.total += profit

        if self.position == '買建':
            action = '売埋'
        elif self.position == '売建':
            action = '買埋'
        else:
            action = '不明'

        transaction['注文番号'] = self.id_order
        transaction['時刻'] = t_current
        transaction['売買'] = action
        transaction['金額'] = self.price * self.unit
        transaction['損益'] = profit
        transaction['最大益'] = self.profit_max
        transaction['最大損'] = self.loss_max
        transaction['備考'] = note

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

        transaction['注文番号'] = self.id_order
        transaction['時刻'] = t_current
        transaction['売買'] = self.position
        transaction['金額'] = self.price * self.unit
        transaction['損益'] = ''
        transaction['最大益'] = ''
        transaction['最大損'] = ''
        transaction['備考'] = note

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
