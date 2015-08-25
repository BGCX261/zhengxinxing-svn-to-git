#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Money import *

class TestMoney(unittest.TestCase):

    def setUp(self):
        self.money = Money()

    def testEquality(self):
        self.assertTrue(self.money.dollar(9).__eq__(self.money.dollar(9)))
        self.assertFalse(self.money.dollar(8).__eq__(self.money.dollar(9)))
        self.assertFalse(self.money.dollar(5).__eq__(self.money.franc(5)))
        self.assertTrue(self.money.franc(9).__eq__(self.money.franc(9)))
        self.assertFalse(self.money.franc(8).__eq__(self.money.franc(9)))

    def testGetCurrency(self):
        self.assertEqual('USD', self.money.dollar(1).getCurrency())
        self.assertEqual('CHF', self.money.franc(1).getCurrency())

    def testMulplification(self):
        dollar = self.money.dollar(5)
        self.assertEqual(self.money.dollar(10), dollar.times(2))
        self.assertEqual(self.money.dollar(15), dollar.times(3))
        f = self.money.franc(5)
        self.assertEqual(self.money.franc(10), f.times(2))
        self.assertEqual(self.money.franc(15), f.times(3))

    def testMoneyAdd(self):
        bank = Bank()
        bank.addRate('CHF', 'USD', 2)

        d5 = self.money.dollar(5)
        d6 = self.money.dollar(6)
        f1 = self.money.franc(1)
        e = d5 + f1
        self.assertEqual(e.__class__, Expression([self.money.dollar(1)]).__class__)
        e = d5 + d6
        self.assertEqual(e.__class__, Expression([self.money.dollar(1)]).__class__)

        d11 = bank.exchange(e, 'USD')
        self.assertEqual(self.money.dollar(11), d11)
        f22 = bank.exchange(e, 'CHF')
        self.assertEqual(self.money.franc(22), f22)

    def testExpressoinMulplification(self):
        e = Expression([self.money.dollar(5)])
        e.times(2)
        self.assertEqual(e, Expression([self.money.dollar(10)]))
        e.times(3)
        self.assertEqual(e, Expression([self.money.dollar(30)]))

        d5=self.money.dollar(5)
        f6 = self.money.franc(6)
        e2 = d5 + f6
        e2.times(2)
        self.assertEqual(e2,
                        self.money.dollar(10) + self.money.franc(12))

        e2 = self.money.dollar(5) + self.money.franc(6)
        e2.times(3)
        self.assertEqual(e2,
                        self.money.dollar(15) + self.money.franc(18))


    def testFailure(self):
        self.assertRaises(NeedListError, Expression, self.money.dollar(1))









if __name__ == '__main__':
    unittest.main()
