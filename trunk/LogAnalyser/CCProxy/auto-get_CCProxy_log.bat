rem %echo off
set app=D:\projects\googlecode\trunk\LogAnalyser\CCProxy\AnalyseCCProxy.py
set web="D:\Program Files\Apache Group\Apache2\htdocs"
set log=F:\temp\新建文件夹\cr-CCProxy\Log
python %app% %log%
copy %log%\CCProxyLog.html %web% /Y
pause