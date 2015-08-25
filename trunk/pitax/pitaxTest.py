#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pitax import *

class PitaxTest(unittest.TestCase):

    def setUp(self):
        pass

    def testSetThreshold(self):
        cal = Pitax()
        self.assertEqual(0, cal.getThreshold())
        cal.setThreshold(1000)
        self.assertEqual(1000, cal.getThreshold())


    def testFeed(self):
        cal = Pitax()
        cal.setThreshold(1600)
        self.assertEqual(cal.feed(0), 0.0)
        self.assertEqual(cal.feed(1501), 0.0)
        self.assertEqual(cal.feed(1900), 15.0)
        self.assertEqual(cal.feed(3759), 198.85)
        self.assertEqual(cal.feed(4000), 235)
        self.assertEqual(cal.feed(40000), 8225)
        self.assertEqual(cal.feed(90010), 24989)
        self.assertEqual(cal.feed(100010), 28989)


if __name__ == '__main__' :
    unittest.main()