#!/usr/bin/env python
# -*- coding: gb2312 -*-

import win32service
# win32serviceutil所提供的功能与win32service相同，但是界面更加友好
# 由于一个操作系统一般只有一个SCM，故而win32serviceutil帮助用户取得
# 该SCM的句柄，而各种针对服务的操作，也只需要提供服务名称即可
import win32serviceutil

##
# 这是一个辅助函数，用于将服务状态的字段翻译出来
# 摘抄自 《Python Programming on Win32》
##
def PrintServiceStatus(status):
    print ''
    svcType, svcState, svcControls, err, svcErr, svcCP, svcWH = status
    if svcType & win32service.SERVICE_WIN32_OWN_PROCESS:
        print "The service runs in its own process"
    if svcType & win32service.SERVICE_WIN32_SHARE_PROCESS:
        print "The service shares a process with other services"
    if svcType & win32service.SERVICE_INTERACTIVE_PROCESS:
        print "The service can interact with the desktop"
    # Other svcType flags not shown.

    if svcState==win32service.SERVICE_STOPPED:
        print "The service is stopped"
    elif svcState==win32service.SERVICE_START_PENDING:
        print "The service is starting"
    elif svcState==win32service.SERVICE_STOP_PENDING:
        print "The service is stopping"
    elif svcState==win32service.SERVICE_RUNNING:
        print "The service is running"
    # Other svcState flags not shown.

    if svcControls & win32service.SERVICE_ACCEPT_STOP:
        print "The service can be stopped"
    if svcControls & win32service.SERVICE_ACCEPT_PAUSE_CONTINUE:
        print "The service can be paused"

##
# 这是一个辅助函数，用于查询某个service是否在运行状态
##
def isServiceRunning(serviceName):
    return win32serviceutil.QueryServiceStatus(serviceName)[1] == 4

def sc(serviceName):
    # 获取“服务管理器”的句柄
    scHandle = win32service.OpenSCManager(None, None,
        win32service.SC_MANAGER_ALL_ACCESS)
    # do something ...
    print 'got SCM handle : %(scHandle)s' % locals()

    # 获取某个服务的句柄
    serviceHandle = win32service.OpenService(scHandle, serviceName,
        win32service.SC_MANAGER_ALL_ACCESS)

    # 利用句柄查询该服务的状态信息
    status = win32service.QueryServiceStatus(serviceHandle)
    PrintServiceStatus(status)

    # 也可以直接通过服务的名称来查询状态
    status = win32serviceutil.QueryServiceStatus(serviceName)

    # 停止该服务
    if isServiceRunning(serviceName):
        status = win32service.ControlService(serviceHandle, win32service.SERVICE_CONTROL_STOP)
        PrintServiceStatus(status)

    # 启动该服务
    if not isServiceRunning(serviceName):
        win32serviceutil.StartService(serviceName)
        PrintServiceStatus(win32serviceutil.QueryServiceStatus(serviceName))

    # 释放所取得的所有句柄
    win32service.CloseServiceHandle(serviceHandle)
    win32service.CloseServiceHandle(scHandle)

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
        win32service.SERVICE_DEMAND_START,
        win32service.SERVICE_ERROR_NORMAL,      # error control type
        appName,
        None,
        0,
        None,
        None,
        None)

    # 释放所取得的所有句柄
    win32service.CloseServiceHandle(hs)
    win32service.CloseServiceHandle(scHandle)


if __name__=='__main__':
    serviceName = 'svnserve'
    svn = 'D:\\Program Files\\Subversion\\bin\\svnserve.exe --service -r g:\\svn'
    createService(serviceName, svn)
    sc('svnserve')
