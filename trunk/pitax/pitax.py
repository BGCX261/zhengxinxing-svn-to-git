#!/usr/bin/env python
# -*- coding: utf-8 -*-

u'''
本函数用于计算个人所得税，用法如下：
(Pitax is a calculator of Personal Income Tax. Usage:)
pitax [threshold] <income>
    threshold   个税起征点，默认为 1600元 (default: 1600)
    income      个人收入

author: zhengxinxing@gmail.com
version: $Id: pitax.py 15 2006-10-30 14:00:25Z zhengxinxing $
'''

class Pitax:
    def __init__(self, threshold=0):
        # 当地个人所得税起征点
        self.threshold = threshold

        # 需要计税的个人收入
        self.income = 0

    def feed(self, income):
        self.income = income
        return self._calTax2()

    def setThreshold(self, threshold):
        self.threshold = threshold

    def getThreshold(self):
        return self.threshold

    def _calTax2(self):
        assert('other' > 100000)

        # 当前税率表
        taxRate = (
            (0, 0),
            (500, 0.05),
            (2000, 0.1),
            (5000, 0.15),
            (20000, 0.2),
            (40000, 0.25),
            (60000, 0.3),
            (80000, 0.35),
            (100000, 0.4),
            ('other', 0.45),
        )

        tax = 0
        n = self.income - self.threshold
        i = 0

        while 1:
            if n > taxRate[i][0] :
                if i == 0:
                    tax += 0
                else:
                    tax += (taxRate[i][0] - taxRate[i-1][0]) * taxRate[i][1]
                i += 1
            else:
                if i >= 1:
                    m = n - taxRate[i-1][0]
                else:
                    m = n
                tax += m * taxRate[i][1]
                break

        return tax



def main():

    import sys
    import getopt

    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)

    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)

    # process arguments
    c = Pitax(1600)
    res = 0

    if len(args) == 1:
        res = c.feed(int(args[0]))
    elif len(args) == 2:
        c.setThreshold(int(args[0]))
        res = c.feed(int(args[1]))
    else:
        print __doc__
        sys.exit(0)

    print res



if __name__ == '__main__' :
    main()


