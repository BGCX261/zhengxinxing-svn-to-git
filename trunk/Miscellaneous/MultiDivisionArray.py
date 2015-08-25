#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
��̬��ά���鼰������
wriiten by ֣����
$Id: MultiDivisionArray.py 27 2006-11-15 13:31:55Z zhengxinxing $
'''

class MyArrayError(Exception): pass
class DivisionError(MyArrayError): pass

class MyArray:
    '''��̬��ά���飬����������ʱָ��ά��
һ����ʼ��֮�󣬶��󼴲��ɸı�
�� class ʵ���˼ӡ�������������������'''

    def __init__(self, row = 1, col = 1, init_action = 'default'):
        self.row = row
        self.col = col
        self.arrays = []
        self.initArrays(init_action)

    ##
    # ��ʼ����ά����
    ##
    def initArrays(self, action):
        # ����ά���鸳��Ĭ��ֵ��ȫ��
        if action == 'default':
            for row in range(self.row):
                rows = []
                for col in range(self.col):
                    rows.append(0)
                self.arrays.append(rows)

        # ���û�ͨ���ַ�������������ֵ
        elif action == 'user':
            for row in range(self.row):
                rows = []
                for col in range(self.col):
                    amount = raw_input('(%s-%s)- ' % (row+1, col+1))
                    while not amount.isdigit():
                        amount = raw_input('(%s-%s)- ' % (row+1, col+1))
                    rows.append(int(amount))
                self.arrays.append(rows)
        else:
            pass


    def checkValid(self, object):
        if object.row == self.row and object.col==self.col:
            return
        raise DivisionError


    def __add__(self, object):
        self.checkValid(object)
        newObject = MyArray(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                newObject.arrays[i][j] = self.arrays[i][j] + object.arrays[i][j]
        return newObject

    def __sub__(self, object):
        self.checkValid(object)
        newObject = MyArray(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                newObject.arrays[i][j] = self.arrays[i][j] - object.arrays[i][j]
        return newObject

    def __mul__(self, object):
        self.checkValid(object)
        newObject = MyArray(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                newObject.arrays[i][j] = self.arrays[i][j] * object.arrays[i][j]
        return newObject

    ##
    # �����ʺ�����ĸ�ʽ
    ##
    def __str__(self):
        s = '\n'
        for i in range(self.col):
            s += '-----'
        s += '-\n'

        for i in range(self.row):
            for j in range(self.col):
                s += '%4s, ' % (self.arrays[i][j])
            s += '\n'
            for i in range(self.col):
                s += '-----'
            s += '-\n'
        return s



if __name__ == '__main__':
    a = MyArray(row = 2, col = 2 )
    print a

    b = MyArray(row = 2, col = 2, init_action = 'user')
    print b

    c = a + b
    d = a - b
    e = a * b
    print c, d, e