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
echo Attempting Intalling Picosettings app...
for %%i in ("%~dp0\Apks\Region\*.apk") do (
 	
 	%adb% install -t -r -d "%%i"
)

Echo Current Region is set to: 
%adb% shell settings get global user_settings_initialized


pause
