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
echo Attempting region change US
%adb% shell settings put global user_settings_initialized US
echo Attempting Clearing cache
%adb% shell pm clear com.picovr.store
%adb% shell pm clear com.picovr.vrusercenter
%adb% shell pm clear com.pvr.home
echo attempting uninstall
%adb% shell pm uninstall -k --user 0 com.picovr.store
%adb% shell pm uninstall -k --user 0 com.picovr.vrusercenter
%adb% shell pm uninstall -k --user 0 com.pvr.home
echo attempting reinstall 
%adb% shell pm install-existing com.picovr.vrusercenter
%adb% shell pm install-existing com.pvr.home
%adb% shell pm install-existing com.picovr.store

echo Attempting store Install...
for %%i in ("%~dp0\Apks\Global\*.apk") do (
 	
 	%adb% install -t -r -d "%%i"
)


echo Attempting to install Matrix...
for %%i in ("%~dp0\Apks\Matrix\*.apk") do (
 	
 	%adb% install -t -r -d "%%i"
)


echo Successfully Installed Store Apps Please - clear update and data using pico settings of the pui matrix...

echo =============Made by owomushi, free to use, no need to pay for it!======================================
echo =============please manually delete data using system settings app on pico!
echo ===========Please delete data for = Store , vrusercenter , matrix ==========================
echo Please manually switch region using pico settings
Echo Current Region is set to: 
%adb% shell settings get global user_settings_initialized
pause
