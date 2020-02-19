import random


class Portfolio:
    cash = 0
    instruments = []
    historyList = []

    def __init__(self):
        self.cash = 500
        history = []
        history.append('Initiated portfolio with 500$ cash.\n')
        self.historyList = history

    def __str__(self):
        cashDetails = 'Cash:\n' + str(self.cash) + "$"
        stockDetails = 'Stock:'
        mutualFundDetails = 'Mutual Fund:'
        bondDetails = 'Bond:'
        if len(self.instruments) == 0:
            return cashDetails + '\nNo instruments.'

        for instrument in self.instruments:
            if type(instrument) is Stock:
                stockDetails += "\n\t" + str(instrument.amount) + " of " + instrument.symbol + " stock."
            elif type(instrument) is MutualFund:
                mutualFundDetails += "\n\t" + str(instrument.amount) + " of " + instrument.symbol + " mutual fund."
            elif type(instrument) is Bond:
                bondDetails += "\n\t" + str(instrument.amount) + " of " + instrument.symbol + " bond."
            else:
                raise Exception('This should never execute. Instrument type error.')

        details = cashDetails + "\n" + stockDetails + "\n" + mutualFundDetails + "\n" + bondDetails + "\n"
        return details

    def addCash(self, amount):
        if (amount<0):
            raise Exception('Try withdrawing cash...')
        self.cash += amount
        self.historyList.append('Added ' + str(amount) + '$ cash to the portfolio. Now there is ' + str(self.cash) +
                                '$ of cash in the portfolio.\n')

    def withdrawCash(self, amount):
        if (amount < 0):
            raise Exception('No need for a negative sign while withdrawing cash...')
        if self.cash > amount:
            self.cash -= amount
            self.historyList.append('Spent ' + str(amount) + '$ cash from the portfolio. Now there is ' + str(self.cash) + '$ of cash in the portfolio.\n')
        elif self.cash == amount:
            self.cash -= amount
            self.historyList.append('Spent ' + str(amount) + '$ cash from the portfolio. Now there is no cash in the portfolio.\n')
        else:
            self.cash -= amount
            raise Exception('Cannot spend that kind of money. This should not be called anyway, but if it is, now you owe ' + str((-self.cash)) + '$.')

    def buyStock(self, amount, stock):
        price = amount*stock.price
        stock.amount = amount
        if self.cash >= price:
            for instrument in self.instruments:
                if type(instrument) is Stock:
                    if instrument.symbol == stock.symbol:
                        instrument.amount += amount
                        self.historyList.append('Added ' + str(amount) + ' of ' + stock.symbol + ' shares to the portfolio. Now there is ' + str(instrument.amount) + ' of ' + instrument.symbol + ' shares in the portfolio.\n')
                        self.withdrawCash(price)
                        return
            self.instruments.append(stock)
            self.historyList.append('Added ' + str(amount) + ' of ' + stock.symbol + ' shares to the portfolio. Now there is ' + str(stock.amount) + ' of ' + stock.symbol + ' shares in the portfolio.\n')
            self.withdrawCash(price)
        else:
            raise Exception('Sorry mate, you do not have the money!')


    def sellStock(self, symbol, amount):
        for instrument in self.instruments:
            if type(instrument) is Stock:
                if instrument.symbol == symbol:
                    if instrument.amount > amount:
                        instrument.amount -= amount
                        self.historyList.append('Sold ' + str(amount) + ' of ' + symbol + ' shares. ' + str(instrument.amount) + ' shares of ' + symbol + ' remain in the portfolio.\n')
                        pricePerShare = instrument.price*random.randint(1,3)/2.0
                        self.historyList.append('Received cash from the sale of ' + symbol + ' shares.\n')
                        self.addCash(pricePerShare*amount)
                        return
                    elif instrument.amount == amount:
                        self.historyList.append('Sold ' + str(amount) + ' of ' + symbol + ' shares. No shares of ' + symbol + ' remain in the portfolio.\n')
                        pricePerShare = instrument.price * random.randint(1, 3) / 2.0
                        self.historyList.append('Received cash from the sale of ' + symbol + ' shares.\n')
                        self.addCash(pricePerShare * amount)
                        self.instruments.remove(instrument)
                        return
                    else:
                        print('You do not own enough of ' + symbol + ' shares. You have currently ' + str(instrument.amount) + ' shares of ' + symbol + '.')
                        return
        raise Exception('You do not own any ' + symbol + ' stock!')

    def buyMutualFund(self, amount, mutualFund):
        price = amount
        mutualFund.amount = amount
        if self.cash >= price:
            for instrument in self.instruments:
                if type(instrument) is MutualFund:
                    if instrument.symbol == mutualFund.symbol:
                        instrument.amount += amount
                        self.historyList.append('Added ' + str(amount) + ' of ' + mutualFund.symbol + ' mutual fund shares to the portfolio. Now there is ' + str(mutualFund.amount) + ' of ' + mutualFund.symbol + ' shares in the portfolio.\n')
                        self.withdrawCash(price)
                        return
            self.instruments.append(mutualFund)
            self.historyList.append('Added ' + str(amount) + ' of ' + mutualFund.symbol + ' mutual fund shares to the portfolio. Now there is ' + str(mutualFund.amount) + ' of ' + mutualFund.symbol + ' shares in the portfolio.\n')
            self.withdrawCash(price)
        else:
            raise Exception('Sorry mate, you do not have the money!')

    def sellMutualFund(self, symbol, amount):
        for instrument in self.instruments:
            if type(instrument) is MutualFund:
                if instrument.symbol == symbol:
                    if instrument.amount > amount:
                        instrument.amount -= amount
                        self.historyList.append('Sold ' + str(amount) + ' of ' + symbol + ' mutual fund shares. ' + str(instrument.amount) + ' shares of ' + symbol + ' remain in the portfolio.\n')
                        pricePerShare = random.randint(9, 12) / 10.0
                        self.historyList.append('Received cash from the sale of ' + symbol + ' mutual fund shares.\n')
                        self.addCash(pricePerShare * amount)
                        return
                    elif instrument.amount == amount:
                        self.historyList.append('Sold ' + str(amount) + ' of ' + symbol + ' mutual fund shares. No shares of ' + symbol + ' remain in the portfolio.\n')
                        pricePerShare = random.randint(9, 12) / 10.0
                        self.historyList.append('Received cash from the sale of ' + symbol + ' mutual fund shares.\n')
                        self.addCash(pricePerShare * amount)
                        self.instruments.remove(instrument)
                        return
                    else:
                        raise Exception(
                            'You do not own enough of ' + symbol + ' mutual fund shares. You have currently ' + str(instrument.amount) + ' shares of ' + symbol + '.')
                        return
        raise Exception('You do not own any ' + symbol + '  mutual fund shares!')

    def history(self):
        summary = '\nHistory:\n'
        count = 1
        for instance in self.historyList:
            summary += str(count) + '. ' + instance
            count += 1
        print(summary)


class Instrument(object):
    def __init__(self):
        return


class Stock(Instrument):
    symbol = ""
    amount = 1
    price = 0

    def __init__(self, price, symbol):
        self.price = price
        self.symbol = symbol


class MutualFund(Instrument):
    symbol = ""
    amount = 1

    def __init__(self, symbol):
        self.symbol = symbol


class Bond(Instrument):
    symbol = ""
    amount = 0

    def __init__(self, symbol):
        self.symbol = symbol


portfolio = Portfolio()
portfolio.addCash(300.50)
s = Stock(20, "HFH")
portfolio.buyStock(5, s)
mf1 = MutualFund("BRT")
mf2 = MutualFund("GHT")
portfolio.buyMutualFund(10.3, mf1)
portfolio.buyMutualFund(2, mf2)
print(portfolio)
portfolio.sellMutualFund("BRT", 3)
portfolio.sellStock("HFH", 1)
portfolio.withdrawCash(50)
portfolio.history()
