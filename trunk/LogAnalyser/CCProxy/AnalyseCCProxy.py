#!/usr/bin/env python
# -*- coding: gb2312 -*-


'''* AnalyseCCProxy�����ڷ���CCProxy����־����ȡ��ָ����Ա����
* ��ָ��ʱ�䡱�ڵ�������Ϊ��һ��С���������
* Ĭ�ϵġ�ָ����Ա������ָ���������������������
* Ĭ�ϵġ�ָ��ʱ�䡱��ָ�����ϰ�ʱ��
*
* ʹ�÷�����
*     AnalyseCCProxy [options] <file | path>
*
*     options:
*         -h,--help               ���������Ϣ
*
*     file      ָ������־�ļ�
*     path      �����Ŀ¼��������־�ļ�
*
* �����
*     ����һ������ļ���������뱻�������־�ļ���ͬĿ¼�£�
*     ��Դ�ļ�ͬ����ֻ�Ǻ�׺Ϊ .html
*
* ʾ����
*     AnalysCCProxy F:\\CCProxy\\Log
*     AnalysCCProxy F:\\CCProxy\\Log\\log20061011.txt
*
* ���ߣ�֣����
* ��ϵ��zhengxinxing@gmail.com
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
# [2006-10-13 07:58:35] 192.168.1.110 ���� Web GET http://m.es.com/180150.swf
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
            '�α���',
            'ĸ����',
            '��÷��',
            '����',
            '������',
        ]
        self.monitorLists = [
            '����', # for test
            '�����',
            '�¹���',
            '��С��',
            'ղѧ��',
            '��÷��',
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
            'needSummary':0, # �Ƿ���Ҫ�ܽ�������
            'dealWithDir':0, # 1 -- ����Ŀ¼�µ�������־�ļ�
                             # 0 -- ������Ŀ¼�����µ�һ����־�ļ�
            'monitorListEnable':1,  #�Ƿ���ר�ż���Ŀ¼��0��1��
            'hideVIP':1, # �Ƿ�����VIP��������־
        }


    def _getName(self, userName):
        # userName likes 'ĳ.ĳĳ' or 'ĳĳ'
        parts = userName.split('.')
        if len(parts) == 2:
            return parts[1]
        else :
            return parts[0]

    ##
    # �����Ƿ��������ŷ��ʵ���վ
    ##
    def _isInsideTarget(self, target):
        res = 0
        for addr in self.insideAddress:
            if re.search(addr, target):
                res = 1
        return res

    ##
    # �����Ƿ��Ǿ�������
    ##
    def _isVIP(self, name):
        if self.config['hideVIP']:
            return name in self.VIP
        return 0

    ##
    # �����Ƿ��ǡ��ر�����б��������
    ##
    def _isOnMonitorLists(self, name):
        return name in self.monitorLists

    ##
    # �����Ƿ����ϰ�ʱ��
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
    # ȥ��һ��URL��������Ϣ����������URL
    ##
    def _getAddress(self, target):
        '''http://a.b.com/asdf --> http://a.b.com'''
        if re.search('://', target):
            parts = target.split('/')
            return '/'.join(parts[0:3])
        return target.split(':')[0]


    ##
    # �����������ֵ��ڣ�����������
    # �������Ѿ����ڣ�����ֵ���� +1
    ##
    def _updateDict(self, d, s):
        if s in d:
            d[s] += 1
        else:
            d[s] = 1

    ##
    # ���������ڴ�
    ##
    def feed(self, logFile):
        log = file(logFile, 'r')
        lines = log.readlines()
        log.close()

        lastName = '' #�����ظ�URL�Ĵ���
        lastTarget = ''  #�����ظ�URL�Ĵ���

        for line in lines:
            parts = line.split(' ')
            if len(parts)!= 7:
                continue

            # �ظ�URL�Ĵ���
            parts[LOGTARGET] = self._getAddress(parts[LOGTARGET])
            if parts[LOGNAME] == lastName and parts[LOGTARGET] ==lastTarget:
                continue
            lastName = parts[LOGNAME]
            lastTarget = parts[LOGTARGET]

            # ��ȡ��������
            parts[LOGNAME] = self._getName(parts[LOGNAME])

            # ���������
            if not self._isInsideTarget(parts[LOGTARGET]) and \
                not self._isVIP(parts[LOGNAME]) and \
                self._isOnDuty(parts[LOGTIME]) :
                if self.config['needSummary']:
                    self._updateDict(self.summary, parts[LOGNAME])
                self.result.append( '%s %s %s --> %s' % (parts[LOGDATE],
                    parts[LOGTIME],
                    parts[LOGNAME],
                    parts[LOGTARGET]))
                # �����ر����������
                if self.config['monitorListEnable'] and \
                    self._isOnMonitorLists(parts[LOGNAME]):
                    self.monitorResult.append( '%s %s %s --> %s' % (
                        parts[LOGDATE],
                        parts[LOGTIME],
                        parts[LOGNAME],
                        parts[LOGTARGET]))


    ##
    # �����ս����Ϊһ���ַ������Ժ���������س���
    ##
    def output(self):
        s = ''
        if self.config['needSummary']:
            summary = []
            for item in self.summary.items():
                summary.append('%s -- %s ��' % (item[0], item[1]))
            s = '%s%s' % ('''������־ժҪ<br>��ע�����ܲ�OA����˾�����վ��ͨѶ��־δ��¼���ڣ�<br><br>''',
                '<br>\n'.join(summary))
        r = '%s%s' % ('<br><br><br>������־ϸ��<br><br>', '<br>\n'.join(self.result))
        self.result = []
        self.summary.clear()
        return '%s%s' % (s, r)

    def outputMonitorListsResult(self):
        s = '%s%s' % ('<br><br><br>������־<br><br>', '<br>\n'.join(
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


def errMsg(s = '�����д����ο�������ʹ�� --help'):
    print s
    sys.exit(2)


#-----------------------------------------------------------------------------
# main functions are here
#-----------------------------------------------------------------------------

def getLogFiles(p):
    # names of CCProxy 's logs like log20061212.txt
    # ����������һ����־�ļ�
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

        #���濪ʼ�����ʼ�����monitor.html���͵�ָ����ַ
        pass


if __name__=='__main__':
    main()

