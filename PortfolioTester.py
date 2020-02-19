import PortfolioProject
import unittest


class PortfolioTester(unittest.TestCase):

    def testInitialCash(self):
        testPortfolio = Portfolio()
        self.assertEqual(500, testPortfolio.cash)

    def testAddCash(self):
        testPortfolio = Portfolio()
        initCash = testPortfolio.cash
        testPortfolio.addCash(50)
        cashChange = testPortfolio.cash - initCash
        self.assertEqual(50, cashChange)

    def testWithdrawCash(self):
        testPortfolio = Portfolio()
        initCash = testPortfolio.cash
        testPortfolio.withdrawCash(50)
        cashChange = testPortfolio.cash - initCash
        self.assertEqual(-50, cashChange)

    def testStock(self):
        newStock = Stock(50, "TEST")
        self.assertEqual(1, newStock.amount)
        self.assertEqual(50, newStock.price)
        self.assertEqual("TEST", newStock.symbol)

    def testAddStock(self):
        testPortfolio = Portfolio()
        initCash = testPortfolio.cash
        newStock = Stock(50, "TEST")
        testPortfolio.buyStock(1, newStock)
        self.assertEqual(1, len(testPortfolio.instruments))
        self.assertEqual(1, testPortfolio.instruments[0].amount)
        self.assertEqual(50, testPortfolio.instruments[0].price)
        self.assertEqual("TEST", testPortfolio.instruments[0].symbol)
        cashChange = testPortfolio.cash - initCash
        self.assertEqual(-50, cashChange)

    def testSellStock(self):
        testPortfolio = Portfolio()
        newStock = Stock(50, "TEST")
        testPortfolio.buyStock(1, newStock)
        initCash = testPortfolio.cash
        testPortfolio.sellStock("TEST", 1)
        self.assertEqual(0, len(testPortfolio.instruments))
        cashChange = testPortfolio.cash - initCash
        self.assertEqual(50, cashChange)

    def testAddFund(self):
        testPortfolio = Portfolio()
        newFund = MutualFund("TEST")
        testPortfolio.buyMutualFund(1, newFund)
        self.assertEqual(1, len(testPortfolio.instruments))
        self.assertEqual("TEST", testPortfolio.instruments[0].symbol)

    def testSellFund(self):
        testPortfolio = Portfolio()
        newFund = MutualFund("TEST")
        testPortfolio.buyMutualFund(1, newFund)
        testPortfolio.sellMutualFund("TEST", 1)
        self.assertEqual(0, len(testPortfolio.instruments))

    def testHistory(self):
        testPortfolio = Portfolio()#1
        testPortfolio.addCash(50)#2
        newStock = Stock(50, "TEST")
        newFund = MutualFund("TEST")
        testPortfolio.buyStock(1, newStock)#3,4
        testPortfolio.buyMutualFund(1, newFund)#5,6
        testPortfolio.sellStock("TEST", 1)#7,8,9
        testPortfolio.sellMutualFund("TEST", 1)#10,11,12
        self.assertEqual(12, len(testPortfolio.historyList))


if __name__ == '__main__':
  unittest.main()
