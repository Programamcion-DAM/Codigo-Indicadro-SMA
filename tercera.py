# region imports
from AlgorithmImports import *
# endregion

class MeasuredTanGoat(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2022, 1, 1)  # Set Start Date
        #self.SetEndDate(2022,1,1)
        self.SetCash(100000)  # Set Strategy Cash
       
        #self.equity = self.AddEquity("TSLA",Resolution.Daily).Symbol
        self.equity = self.AddForex("EURUSD",Resolution.Daily).Symbol
        
        self.smaLow = self.SMA(self.equity,4,Resolution.Daily)
        self.smaMedium = self.SMA(self.equity,9,Resolution.Daily)
        self.smaHigh = self.SMA(self.equity,18,Resolution.Daily)

        self.state = None

        self.SetWarmUp(20)

    def OnData(self, data: Slice):
        if self.IsWarmingUp:
            return

        price = 0
        if data[self.equity]:
            price = data[self.equity].Close
        else:
            return

        if self.Portfolio.Invested:
            if self.state:
                if not self.smaLow > self.smaMedium > self.smaHigh:
                    self.Liquidate()
            else:
                if not self.smaLow < self.smaMedium < self.smaHigh:
                    self.Liquidate()
            return

        if self.smaLow > self.smaMedium > self.smaHigh:
            self.SetHoldings(self.equity,1)
            self.state = True
            return
        elif self.smaLow < self.smaMedium < self.smaHigh:
            self.SetHoldings(self.equity,-1)
            self.state = False
            return
