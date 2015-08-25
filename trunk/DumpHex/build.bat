@echo off
rem
rem use lcc to build DumpHex.c to .exe
rem
set p=D:\Program files\lcc\bin
set c=%p%\lcc.exe
set l=%p%\lcclnk.exe
echo on
"%c%" DumpHex.c
"%l%" DumpHex.obj