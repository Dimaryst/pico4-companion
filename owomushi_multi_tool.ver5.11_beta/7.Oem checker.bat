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

echo Your oem state is set to:
%adb% shell getprop ro.oem.state
echo If "true" you are oem
echo If blank you are non-oem
Echo Current Region is set to: 
%adb% shell settings get global user_settings_initialized


pause
