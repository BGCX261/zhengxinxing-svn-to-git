#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NumDict:
    def __init__(self, inputs):
        self.data = {}
        if inputs is not None:
            for item in inputs:
                (category, value) = item
                self.increase(category, value)

    def __getitem__(self, key):
        return self.data.get(key, 0)

    def __setitem__(self, key, value):
        self.data[key] = value

    def increase(self, key, value):
        #为了方便使用，允许用户对原先不存在的项目进行increase调用
        # 故而需要使用 .get(key, 0) 这样的语法来做默认值处理
        self.data[key] = self.data.get(key, 0) + value

    def items(self):
        # sort() 操作会影响 list 的内容，所以python设计者故意不让sort有返回值
        l = self.data.keys().sort()
        return l

    def clear(self):
        self.data.clear()


if __name__ == '__main__':
    d = NumDict()
    d['东'] = 50 # 东 == 50
    d.increase('东', 10) # 东 == 60
    d.increase('西', 20) # 西 == 20
    d.items() # ['东', '西']
    d.clear()