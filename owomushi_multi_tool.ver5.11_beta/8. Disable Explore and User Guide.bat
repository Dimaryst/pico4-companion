chcp 65001
@echo off

:Retry
cls
echo ===================================================
echo Waiting for Pico
set adb="%~dp0\ADB\adb.exe"
%adb% devices -l | findstr "PICO">nul && (goto Success)
echo ===================================================
echo Please wait....
pause 0
cls
goto Retry

:Success

echo ===================================================
echo prepairing to install....
echo ===================================================
pause 0
echo Disable Home and activitycenter...


%adb% shell pm disable-user --user 0 com.picovr.activitycenter
%adb% shell pm disable-user --user 0 com.pvr.home
%adb% shell pm disable-user --user 0 com.picovr.guide
 
echo =======like and subscribe to @owomushi on youtube========
pause