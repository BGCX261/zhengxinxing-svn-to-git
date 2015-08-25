#!/usr/bin/env python
# -*- coding: gb2312 -*-

import win32service
import win32serviceutil
import win32event

##
# �� class ��Լ��ȫ������С��һ�� windows service ��ʵ����
# �ο��� ��Python Programming on Win32��
##
class SmallestPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'SmallestPythonService'
    _svc_display_name_ = 'Smallest Python Service'

    def __init__(self, args):
        win32serviceutil.ServiceFranework.__init__(self,args)
        # ����һ��event������ service stop �¼�
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        # ���κ�����֮ǰ����Ҫ��֪ͨSCM
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # Ȼ�󼤻����ǵ� event
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        # �������ѭ�����棬����ʲôҲ������ֻ�ǵ��ű��ɵ�
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)


if __name__=='__main__':
    win32serviceutil.HandleCommandLine(SmallestPythonService)
