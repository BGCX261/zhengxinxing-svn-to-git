rem ���ű��� auto-get_CCProxy_log.bat ����ű����ó�ÿ�հ�ҹ�Զ�����
rem written by ֣���� 2006.11
schtasks  /create  /tn GetCCProxyLog  /sc daily  /st 23:59   /tr D:\projects\googlecode\trunk\LogAnalyser\CCProxy\auto-get_CCProxy_log.bat  