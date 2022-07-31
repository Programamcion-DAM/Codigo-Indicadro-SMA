# region imports
from AlgorithmImports import *
# endregion

class CalculatingFluorescentOrangeGuanaco(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.AddForex("EURUSD", Resolution.Daily)

        self.sma = self.SMA("EURUSD",200,Resolution.Daily)

        self.state = None

        self.SetWarmUp(100)

    def OnData(self, data: Slice):
        if self.IsWarmingUp:
            return

        price = 0
        if data["EURUSD"]:
            price = data["EURUSD"].Close
        else:
            return

        if self.Portfolio.Invested:
            if self.state:
                if price < self.sma.Current.Value:
                    self.Liquidate()
            else:
                if price > self.sma.Current.Value:
                    self.Liquidate()
            return

        if price > self.sma.Current.Value:
            self.SetHoldings("EURUSD",1)
            self.state = True
            return
        else:
            self.SetHoldings("EURUSD",-1)
            self.state = False
            return
