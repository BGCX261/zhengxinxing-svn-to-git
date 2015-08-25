#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MoneyError(Exception): pass
class NoRateError(MoneyError): pass
class NeedListError(MoneyError): pass


class Money:
    def __init__(self, currency='USD', amount=0):
        self.amount = amount
        self.currency = currency

    def __eq__(self, money):
        return ((money.amount == self.amount) and
                (money.getCurrency() == self.getCurrency()))

    def __add__(self, money):
        '''两个Money相加后，将获得一个Expression
        '''
        e = Expression([self])
        e.add(money)
        return e


    def __repr__(self):
        return 'Money-<%s, %s>' % (self.currency, self.amount)


    def dollar(self, amount):
        return Money('USD', amount)

    def franc(self, amount):
        return Money('CHF', amount)

    def getCurrency(self):
        return self.currency

    def times(self, multiplier):
        return Money(self.currency, self.amount * multiplier)


class Bank:
    def __init__(self, rateTable={}):
        self.rateTable = rateTable

    def exchange(self, expression, currency):
        '''将混合的货币集，兑换成指定一种货币输出
        '''
        sum = 0
        for money in expression.wallet:
            rate = self.getRate(money.getCurrency(), currency)
            sum += money.amount / rate
        return Money(currency, sum)

    def addRate(self, source, dest, rate):
        self.rateTable[(source, dest)] = rate

    def getRate(self, source, dest):
        if source == dest:
            return 1

        if (source, dest) in self.rateTable:
            return self.rateTable[(source, dest)]

        if (dest, source) in self.rateTable:
            return 1.0/self.rateTable[(dest, source)]

        raise NoRateError

class Expression:
    def __init__(self, moneys=[]):
        if moneys.__class__ != [].__class__:
            raise NeedListError
        self.wallet = moneys

    def __eq__(self, expression):
        return self.wallet == expression.wallet

    def add(self, money):
        w = self._cp(self.wallet)
        i = self._isCurrencyInWallet(money.getCurrency())
        if i:
            w[i-1].amount += money.amount
        else:
            w.append(money)
            w.sort()
        return Expression(w)

    def times(self, multiplier):
        w = self._cp(self.wallet)
        for money in w:
            money.amount *= multiplier
        return Expression(w)

    def _isCurrencyInWallet(self, currency):
        i = 0
        for money in self.wallet:
            i += 1
            if currency == money.getCurrency():
                return i
        return 0

    def _cp(self, l):
        a = [x for x in l]
        return a

if __name__ == '__main__':
    e = Expression()
    print e.wallet