# region imports
from AlgorithmImports import *
# endregion

class CalculatingFluorescentOrangeGuanaco(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        
        self.active = self.AddForex("EURUSD", Resolution.Daily).Symbol

        self.sma200 = self.SMA(self.active,200,Resolution.Daily)
        self.sma50 = self.SMA(self.active,50,Resolution.Daily)

        self.state = None

        self.SetWarmUp(200)

    def OnData(self, data: Slice):
        if self.IsWarmingUp:
            return

        price = 0
        if data[self.active]:
            price = data[self.active].Close
        else:
            return

        if self.Portfolio.Invested:
            if self.state:
                if self.sma50.Current.Value < self.sma200.Current.Value:
                    self.Liquidate()
            else:
                if self.sma50.Current.Value > self.sma200.Current.Value:
                    self.Liquidate()
            return

        if self.sma50.Current.Value > self.sma200.Current.Value:
            self.SetHoldings(self.active,1)
            self.state = True
            return
        else:
            self.SetHoldings(self.active,-1)
            self.state = False
            return
