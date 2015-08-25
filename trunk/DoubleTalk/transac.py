#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

class Transaction:
    def __init__(self):
        self.date = str(datetime.today())
        self.commet = ''

    def display(self):
        pass

    def addLine(self, transaction, value):
        pass

    def __add__(self, object):
        pass

    def __sub__(self, object):
        pass

    def __mul__(self, object):
        pass

    ##
    # 利用时间对 Transaction 进行排序
    ##
    def __cmp__(self):
        pass

    def __str__(self):
        pass



if __name__ == '__main__':
    from dates import *

    T1 = Transaction()
    T1.date = asc2sec('1/1/1999')
    T1.comment = 'Start the company'
    T1.addLine('MyCo.Assets.NCA.CurAss.Cash', 10000)
    T1.addLine('MyCo.Capital.Shares', -10000)
    T1.validate()
    T1.display()                                   # print to standard output

    T2 = Transaction()
    T2.date = asc2sec('5-Jan-1999')                # four days later...
    T2.comment = 'Loan from Grandma'
    T2.addLine('MyCo.Assets.NCA.CurAss.Cash', 15000)
    T2.addLastLine('MyCo.Assets.OtherLia.Loans')   # addLastLine rounds off the final line for you
    T2.display()

    T3 = T1 + T2   # we can add them together
    T3.display()

    T4 = T1 * 1.2
    T4.display()
