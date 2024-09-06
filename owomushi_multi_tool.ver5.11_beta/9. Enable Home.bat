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
echo Conected Successful

echo reinstall Home
%adb% shell pm install-existing com.picoxr.bstreamassistant
%adb% shell pm install-existing com.pvr.home
%adb% shell pm install-existing com.picovr.activitycenter

echo Attempting store Intall...
for %%i in ("%~dp0\Apks\Global\*.apk") do (
 	
 	%adb% install -t -r -d "%%i"
)


echo =============Made by owomushi, free to use, no need to pay for it!======================================
Echo Current Region is set to: 
%adb% shell settings get global user_settings_initialized
pause
