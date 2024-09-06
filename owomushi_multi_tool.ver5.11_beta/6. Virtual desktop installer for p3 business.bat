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

echo install Virtual desktop


echo Attempting store Intall...
for %%i in ("%~dp0\Apks\Vd\*.apk") do (
 	
 	%adb% install -t -r -d "%%i"
)

echo this will only work with 5.7.5 business pico 3 pro 
echo =============Virtual Desktop dev does not support offically buying this. ======================================
Echo Current Region is set to: 
%adb% shell settings get global user_settings_initialized
pause
