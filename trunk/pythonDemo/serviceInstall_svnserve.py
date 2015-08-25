#!/usr/bin/env python
# -*- coding: utf-8 -*-


import win32service


def createService(serviceName, appName):
    # 获取“服务管理器”的句柄
    scHandle = win32service.OpenSCManager(None, None,
        win32service.SC_MANAGER_ALL_ACCESS)

    # 开始创建
    hs = win32service.CreateService(scHandle,
        serviceName,
        serviceName,
        win32service.SERVICE_ALL_ACCESS,         # desired access
        win32service.SERVICE_WIN32_OWN_PROCESS,  # service type
        win32service.SERVICE_DEMAND_START,      # start type
        win32service.SERVICE_ERROR_NORMAL,      # error control type
        appName,
        None,   0,    None,   None, None  )

    # 释放所取得的所有句柄
    win32service.CloseServiceHandle(hs)
    win32service.CloseServiceHandle(scHandle)


if __name__=='__main__':
    serviceName = 'svnservice'
    svn = 'D:\\Program Files\\Subversion\\bin\\svnserve.exe --service -r g:\\svn'
    createService(serviceName, svn)
