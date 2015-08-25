#!/usr/bin/env python
# -*- coding: gb2312 -*-

import win32service
import win32serviceutil
import win32event

##
# 本 class 大约是全世界最小的一个 windows service 的实现了
# 参考自 《Python Programming on Win32》
##
class SmallestPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'SmallestPythonService'
    _svc_display_name_ = 'Smallest Python Service'

    def __init__(self, args):
        win32serviceutil.ServiceFranework.__init__(self,args)
        # 创建一个event，用于 service stop 事件
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        # 做任何事情之前，都要先通知SCM
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 然后激活我们的 event
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        # 在这个主循环里面，我们什么也不做，只是等着被干掉
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)


if __name__=='__main__':
    win32serviceutil.HandleCommandLine(SmallestPythonService)
