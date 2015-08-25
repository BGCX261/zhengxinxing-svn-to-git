#!/usr/bin/env python
# -*- coding: gb2312 -*-

import win32service
# win32serviceutil���ṩ�Ĺ�����win32service��ͬ�����ǽ�������Ѻ�
# ����һ������ϵͳһ��ֻ��һ��SCM���ʶ�win32serviceutil�����û�ȡ��
# ��SCM�ľ������������Է���Ĳ�����Ҳֻ��Ҫ�ṩ�������Ƽ���
import win32serviceutil

##
# ����һ���������������ڽ�����״̬���ֶη������
# ժ���� ��Python Programming on Win32��
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
# ����һ���������������ڲ�ѯĳ��service�Ƿ�������״̬
##
def isServiceRunning(serviceName):
    return win32serviceutil.QueryServiceStatus(serviceName)[1] == 4

def sc(serviceName):
    # ��ȡ��������������ľ��
    scHandle = win32service.OpenSCManager(None, None,
        win32service.SC_MANAGER_ALL_ACCESS)
    # do something ...
    print 'got SCM handle : %(scHandle)s' % locals()

    # ��ȡĳ������ľ��
    serviceHandle = win32service.OpenService(scHandle, serviceName,
        win32service.SC_MANAGER_ALL_ACCESS)

    # ���þ����ѯ�÷����״̬��Ϣ
    status = win32service.QueryServiceStatus(serviceHandle)
    PrintServiceStatus(status)

    # Ҳ����ֱ��ͨ���������������ѯ״̬
    status = win32serviceutil.QueryServiceStatus(serviceName)

    # ֹͣ�÷���
    if isServiceRunning(serviceName):
        status = win32service.ControlService(serviceHandle, win32service.SERVICE_CONTROL_STOP)
        PrintServiceStatus(status)

    # �����÷���
    if not isServiceRunning(serviceName):
        win32serviceutil.StartService(serviceName)
        PrintServiceStatus(win32serviceutil.QueryServiceStatus(serviceName))

    # �ͷ���ȡ�õ����о��
    win32service.CloseServiceHandle(serviceHandle)
    win32service.CloseServiceHandle(scHandle)

def createService(serviceName, appName):
    # ��ȡ��������������ľ��
    scHandle = win32service.OpenSCManager(None, None,
        win32service.SC_MANAGER_ALL_ACCESS)

    # ��ʼ����
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

    # �ͷ���ȡ�õ����о��
    win32service.CloseServiceHandle(hs)
    win32service.CloseServiceHandle(scHandle)


if __name__=='__main__':
    serviceName = 'svnserve'
    svn = 'D:\\Program Files\\Subversion\\bin\\svnserve.exe --service -r g:\\svn'
    createService(serviceName, svn)
    sc('svnserve')
