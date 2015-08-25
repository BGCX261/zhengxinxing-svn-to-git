#!/usr/bin/env python
# -*- coding: utf-8 -*-
u'''本代码主要演示了程序参数的使用：
 1. 从文件和命令行中获取配置信息，体现两者的一致性
 2. 允许程序运行过程中，动态改变参数
 3. 展示了类对象对参数的引用方式、修改方式
 4. 所涉及的参数，包括“选项”、“参数”两种

鉴于参数主要是 class 在使用，故而其 default 值应该由 class 负责处理，
而 main() 函数只是负责对用户的输入进行标准化处理。
另外，程序的配置文件相关参数，也完全由 class 来处理


$Id: config.py 36 2006-11-30 09:13:15Z zhengxinxing $
'''

import sys
import getopt
import re
import string
import unittest
import ConfigParser


##############################################################################
#  本 class 实现了对配置信息的基本处理，包括默认值、配置文件和命令
# 行参数三种配置信息来源。使用的例子见后面的 ClientDemo 类
##############################################################################
class Config:
    def __init__(self, default={}, valueRange={}):
        self.config = default
        self.range = valueRange

    def __getitem__(self, item):
        return self.config[item]

    def __setitem__(self, item, value):
        self.config[item] = value

    ##
    # 从配置文件中获取配置信息
    # 将 section.option 及其对应的值写入字典
    ##
    def mergeFromFile(self, file):
        cp = ConfigParser.ConfigParser(  )
        cp.read(file)
        for sec in cp.sections(  ):
            for opt in cp.options(sec):
                name = string.lower(sec) + "." + string.lower(opt)
                value = string.strip( cp.get(sec, opt) )
                # 如果配置项不在“所有选项”里面，则认为是拼写错误，予以丢弃
                if name not in self.config:
                    continue
                    
                # 如果是“开关项”，则强制要求用0 、1 来表示其值
                if self.config[name] in [True, False]:
                    if value not in ['0', '1']:
                        continue
                    if value == '0':
                        self.config[name] = False
                    else:
                        self.config[name] = True
                    continue
                    
                # 如果获取到的值不在允许的范围内，则认为设置错误，予以丢弃
                #...?
                if not re.search(self.range[name], value):
                    continue
                
                self.config[name] = value

    ##
    # 本函数将用户输入的命令行参数合并进来。要求命令行参数经过 getopt 模块
    # 的处理，获得如下形式的输入：
    # [('system.is_debug', ''), ('system.log', '2')]
    # 注意：上述输入中，参数名是经过客户端代码处理过的
    ##
    def mergeFromOptions(self, options=[]):
        for option, value in options:
            if value != '':
                if not re.search(self.range[option], value):
                    continue
                self.config[option] = value
            else:
                # 遇见无值的，应该是开关选项，如 debug 等
                # 因此，需要参考默认值进行反置处理
                if self.config[option] == True:
                    self.config[option] = False
                else:
                    self.config[option] = True

    def items(self):
        return self.config.items()
        
    def set(self, item, value):
        #检测 value，看是否在允许范围内
        # ...?
        
        if not re.search(self.range[item], value):            
            return 
        self.config[item] = value

##############################################################################
# 这是一个用于辅助实现针对 Config 类的 unit test 的类
##############################################################################
class ConfigTestAssist:
    def __init__(self, options=[]):

        # 给出所有选项及其默认值
        defaultValue = {
            'system.is_debug': False,
            'system.log_level': '2',
            'system.name': 'Rose',
        }
        # 值的范围该如何给出比较合适？?
        valueRange = {
            'system.is_debug': 'False|True',
            'system.log_level': '0|1|2',
            'system.name': '.*',
        }
        self.config = Config(defaultValue, valueRange)

        # 给出命令行参数对应的选项名，并利用之格式化用户输入
        formalOptions = {
            '-d':'system.is_debug',
            '--debug':'system.is_debug',
            '-l':'system.log_level',
            '--log':'system.log_level',
        }
        self.options = [(formalOptions[o], v) for o,v in options]

    ###
    # 测试用的函数
    ###
    def _mergeFromFile(self, file='config.ini'):
        self.config.mergeFromFile(file)

    ###
    # 测试用的函数
    ###
    def _mergeFromOptions(self):
        self.config.mergeFromOptions(self.options)

##############################################################################
# 用于测试 Config 类的 unit test 代码
##############################################################################
class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.a = ConfigTestAssist()
        self.b = ConfigTestAssist([('-d','')])
        self.c = ConfigTestAssist([('--log','0')])

    def testTriggerOptions(self):
        self.assertFalse(self.a.config['system.is_debug'])
        self.a._mergeFromFile()
        self.assertTrue(self.a.config['system.is_debug'])

        self.assertFalse(self.b.config['system.is_debug'])
        self.b._mergeFromOptions()
        self.assertTrue(self.b.config['system.is_debug'])

    def testValueOptions(self):
        self.assertEqual(self.c.config['system.log_level'], '2')
        self.c._mergeFromOptions()
        self.assertEqual(self.c.config['system.log_level'], '0')
        
        
    ###
    # 用于保证，当配置文件出现错误配置项、错误配置值的时候，可以得到适当的处理
    # 由于命令行参数有 getopt 在控制，因此不会出现错误选项，最多出现错误值
    ###
    def testWrongConfigFile(self):
        # 首先，如果配置文件存在错误的配置项，则不予理睬
        pass
        
    def testWrongValue(self):
        # log_level 允许的值是('0', '1', '2')，超出范围者，则给予默认值
        d = ConfigTestAssist([('--log','3')])
        d._mergeFromOptions()
        self.assertEqual(d.config['system.log_level'], '2')
        
    def testSet(self):
        self.assertEqual(self.a.config['system.name'], 'Rose')
        self.a.config.set('system.name', 'Mike')
        self.assertEqual(self.a.config['system.name'], 'Mike')
        
        self.a.config.set('system.log_level', '3')
        self.assertEqual(self.a.config['system.log_level'], '2')
        
        self.a.config.set('system.log_level', '1')
        self.assertEqual(self.a.config['system.log_level'], '1')


##############################################################################
# 客户端代码示例。实际使用中，需要修改的有以下几处：
# 1. 配置文件名
# 2. 所有选项及其默认值、值的范围
#   2.1 选项分为“开关项”、字符串 两种类型
#   2.2 若是开关项，务必使用True/False作为默认值，且使用 is 作为变量名前缀
# 3. 所有命令行参数及其对应的正规选项名
# 4. 参考第3点，修改getOptions() 函数中的 getopt() 函数参数
##############################################################################
class ClientDemo:
    def __init__(self, options=[]):
        # 给出配置文件的名称
        self.configFile = 'config.ini'

        # 给出所有选项及其默认值
        defaultValue = {
            'system.is_debug':False,
            'system.log_level': 'normal',
            'system.name': 'no name'
        }
        valueRange = {
            'system.is_debug': 'False|True',
            'system.log_level': 'less|normal|redundant',
            'system.name': '.*',
        }
        self.config = Config(defaultValue, valueRange)

        # 给出命令行参数对应的选项名，并利用之格式化用户输入
        formalOptions = {
            '-d':'system.is_debug',
            '--debug':'system.is_debug',
            '-l':'system.log_level',
            '--log':'system.log_level',
        }
        options = getOptions()
        self.options = [(formalOptions[o], v) for o,v in options]

        self.setConfig(self.options)

    ###
    # 类初始化辅助函数
    ###
    def setConfig(self, options):
        # 读取配置文件
        self.config.mergeFromFile(self.configFile)

        # 解析用户输入的参数
        self.config.mergeFromOptions(options)

    ###
    # 类初始化辅助函数，解析命令行内容，其包括“选项”和“参数”两块内容
    # 目前本函数仅对“选项”进行处理，“参数”未处理
    ###
    def getOptions(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:],
                "dhl:",
                ['debug', "help", 'log'])
        except getopt.error, msg:
            print 'options error, for help use --help'
            sys.exit(2)

        return opts

    def doSomething(self):
        # 配置项的使用
        if self.config['system.is_debug'] :
            print 'debug on'
        else:
            print 'debug off'
        
        if self.config['system.log_level'] == 'less':
            print 'log level 1'
        elif self.config['system.log_level'] == 'normal':
            print 'log level 2'            
        elif self.config['system.log_level'] == 'redundant':
            print 'log level 3'
            # 运行时修改配置项
            self.config.set('system.log_level', 'less')


if __name__ == '__main__' :
    unittest.main()


