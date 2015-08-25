#!/usr/bin/env python
# -*- coding: gb2312 -*-


'''* AnalyseCCProxy是用于分析CCProxy的日志，提取“指定人员”在
* “指定时间”内的上网行为的一个小工具软件。
* 默认的“指定人员”，是指除各部门主管外的其他人
* 默认的“指定时间”，指的是上班时间
*
* 使用方法：
*     AnalyseCCProxy [options] <file | path>
*
*     options:
*         -h,--help               输出帮助信息
*
*     file      指定的日志文件
*     path      处理该目录下所有日志文件
*
* 输出：
*     生成一个结果文件，存放在与被处理的日志文件相同目录下，
*     与源文件同名，只是后缀为 .html
*
* 示例：
*     AnalysCCProxy F:\\CCProxy\\Log
*     AnalysCCProxy F:\\CCProxy\\Log\\log20061011.txt
*
* 作者：郑新星
* 联系：zhengxinxing@gmail.com
*
* $Id: AnalyseCCProxy.py 46 2007-07-19 14:04:46Z zhengxinxing $
'''


import sys
import getopt
import re
import os
from os.path import isfile
from os.path import isdir
from os import listdir
from datetime import date

#      0          1            2        3   4   5            6
# [2006-10-13 07:58:35] 192.168.1.110 李四 Web GET http://m.es.com/180150.swf
LOGDATE = 0
LOGTIME = 1
LOGADDR = 2
LOGNAME = 3
LOGPROXY = 4
LOGACTION = 5
LOGTARGET = 6


class LogAnalyser:

    def __init__(self):
        self.timeslices = [
            ('08:00:00', '11:50:00'),
            ('13:30:00', '17:30:00'),
        ]
        self.VIP = [
            '何宝庆',
            '母世杰',
            '张梅钦',
            '朱哲',
            '钟永成',
        ]
        self.monitorLists = [
            '马六', # for test
            '俞积彬',
            '陈光领',
            '吴小荣',
            '詹学清',
            '杨梅洪',
        ]
        self.monitorResult = []
        self.insideAddress = [
            '192\.168\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?',
            '127\.0\.0\.1',
            '0\.0\.0\.0',
            '220\.160\.108\.13[0-4]',
            '2mobi\.cn',
            'yaxon\.com',
            'anygonavi\.com',
        ]
        self.result = []
        self.summary = {}
        self.config = {
            'needSummary':0, # 是否需要总结性文字
            'dealWithDir':0, # 1 -- 处理目录下的所有日志文件
                             # 0 -- 仅处理目录下最新的一个日志文件
            'monitorListEnable':1,  #是否处理专门监视目录，0否，1是
            'hideVIP':1, # 是否隐藏VIP的上网日志
        }


    def _getName(self, userName):
        # userName likes '某.某某' or '某某'
        parts = userName.split('.')
        if len(parts) == 2:
            return parts[1]
        else :
            return parts[0]

    ##
    # 看看是否是允许开放访问的网站
    ##
    def _isInsideTarget(self, target):
        res = 0
        for addr in self.insideAddress:
            if re.search(addr, target):
                res = 1
        return res

    ##
    # 看看是否是经理级人物
    ##
    def _isVIP(self, name):
        if self.config['hideVIP']:
            return name in self.VIP
        return 0

    ##
    # 看看是否是“特别监视列表”里面的人
    ##
    def _isOnMonitorLists(self, name):
        return name in self.monitorLists

    ##
    # 看看是否是上班时间
    ##
    def _isOnDuty(self, logTime):
        #  '09:09:09]' --> '09:09:09'
        t = logTime[0:-1]
        onDuty = 0

        # '09:09:09' in ('08:00:00', '11:50:00') ?
        for slice in self.timeslices:
            if t>slice[0] and t<slice[1] :
                onDuty = 1

        return onDuty


    ##
    # 去除一个URL的子项信息，保留基本URL
    ##
    def _getAddress(self, target):
        '''http://a.b.com/asdf --> http://a.b.com'''
        if re.search('://', target):
            parts = target.split('/')
            return '/'.join(parts[0:3])
        return target.split(':')[0]


    ##
    # 若参数不在字典内，则予以新增
    # 若参数已经在内，则将其值予以 +1
    ##
    def _updateDict(self, d, s):
        if s in d:
            d[s] += 1
        else:
            d[s] = 1

    ##
    # 主处理函数在此
    ##
    def feed(self, logFile):
        log = file(logFile, 'r')
        lines = log.readlines()
        log.close()

        lastName = '' #用于重复URL的处理
        lastTarget = ''  #用于重复URL的处理

        for line in lines:
            parts = line.split(' ')
            if len(parts)!= 7:
                continue

            # 重复URL的处理
            parts[LOGTARGET] = self._getAddress(parts[LOGTARGET])
            if parts[LOGNAME] == lastName and parts[LOGTARGET] ==lastTarget:
                continue
            lastName = parts[LOGNAME]
            lastTarget = parts[LOGTARGET]

            # 获取正规名字
            parts[LOGNAME] = self._getName(parts[LOGNAME])

            # 主处理语句
            if not self._isInsideTarget(parts[LOGTARGET]) and \
                not self._isVIP(parts[LOGNAME]) and \
                self._isOnDuty(parts[LOGTIME]) :
                if self.config['needSummary']:
                    self._updateDict(self.summary, parts[LOGNAME])
                self.result.append( '%s %s %s --> %s' % (parts[LOGDATE],
                    parts[LOGTIME],
                    parts[LOGNAME],
                    parts[LOGTARGET]))
                # 处理“特别监视名单”
                if self.config['monitorListEnable'] and \
                    self._isOnMonitorLists(parts[LOGNAME]):
                    self.monitorResult.append( '%s %s %s --> %s' % (
                        parts[LOGDATE],
                        parts[LOGTIME],
                        parts[LOGNAME],
                        parts[LOGTARGET]))


    ##
    # 将最终结果作为一个字符串，以函数结果返回出来
    ##
    def output(self):
        s = ''
        if self.config['needSummary']:
            summary = []
            for item in self.summary.items():
                summary.append('%s -- %s 次' % (item[0], item[1]))
            s = '%s%s' % ('''网络日志摘要<br>（注：与总部OA、公司相关网站的通讯日志未记录在内）<br><br>''',
                '<br>\n'.join(summary))
        r = '%s%s' % ('<br><br><br>网络日志细节<br><br>', '<br>\n'.join(self.result))
        self.result = []
        self.summary.clear()
        return '%s%s' % (s, r)

    def outputMonitorListsResult(self):
        s = '%s%s' % ('<br><br><br>上网日志<br><br>', '<br>\n'.join(
                      self.monitorResult))
        self.monitorResult = []
        return s

#-----------------------------------------------------------------------------
# reusable functions are here
#-----------------------------------------------------------------------------
def chooseFile(path, mark):
    ''' search files in path that the file name has some mark '''
    files = os.listdir(path)
    s = re.compile(mark, re.IGNORECASE)
    files = filter(s.search, files)
    toFullName = lambda f: path + '\\' + f
    return map(toFullName, files)


def errMsg(s = '参数有错，欲参考帮助请使用 --help'):
    print s
    sys.exit(2)


#-----------------------------------------------------------------------------
# main functions are here
#-----------------------------------------------------------------------------

def getLogFiles(p):
    # names of CCProxy 's logs like log20061212.txt
    # 仅输出最近的一个日志文件
    files = chooseFile(p, '^log[0-9]{8}\.txt')
    files.sort()
    return [files[-1],]


def getOutputFileName(f):
    #return f[0:-3] + 'html'

    return '%s\\CCProxyLog.html' % ( os.path.split(f)[0] )


def main():

    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ['help'])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)

    # process options
    if len(opts) >= 2 :
        errMsg()
    for o, arg in opts:
        if o in ("-h", "--help"):
            errMsg()

    # process arguments
    files = []
    if len(args) == 0 :
        files.append('.\\log20061013.txt')
    elif (len(args)==1 and isfile(args[0])):
        files.append(args[0])
    elif len(args) == 1 and isdir(args[0]):
        files = getLogFiles(args[0])
    else:
        errMsg()

    # main steps
    ana = LogAnalyser()
    for file in files:
        ana.feed(file)
        f = open(getOutputFileName(file), 'w')
        f.write(ana.output())
        f.close()

        f = open('monitor.html', 'w')
        f.write(ana.outputMonitorListsResult())
        f.close()

        #下面开始发送邮件，将monitor.html发送到指定地址
        pass


if __name__=='__main__':
    main()

