rem 本脚本将 auto-get_CCProxy_log.bat 这个脚本设置成每日半夜自动运行
rem written by 郑新星 2006.11
schtasks  /create  /tn GetCCProxyLog  /sc daily  /st 23:59   /tr D:\projects\googlecode\trunk\LogAnalyser\CCProxy\auto-get_CCProxy_log.bat  