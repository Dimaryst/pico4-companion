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
echo attempting uninstall of business apps
%adb% shell pm uninstall -k --user 0 com.pvr.tobactivate
%adb% shell pm uninstall -k --user 0 com.picovr.tobvrusercenter
%adb% shell pm uninstall -k --user 0 com.pvr.tobhome
%adb% shell pm uninstall -k --user 0 com.pvr.tobstore
%adb% shell pm uninstall -k --user 0 com.pvr.tobservice
%adb% shell pm uninstall -k --user 0 com.picovr.enterpriseassistant 

echo attempting reinstall 
%adb% shell pm install-existing com.picovr.vrusercenter
%adb% shell pm install-existing com.pvr.home
%adb% shell pm install-existing com.picovr.store

echo Attempting Global store Install...
for %%i in ("%~dp0\Apks\Global\*.apk") do (
 	
 	%adb% install -t -r -d "%%i"
)

echo Successfully installed Global store...

echo Attempting Launcher Install...
for %%i in ("%~dp0\Apks\Business\*.apk") do (
 	
 	%adb% install -t -r -d "%%i"
)

echo please Run after pico reboots  
echo Please Please use Lighting launcher to open store


echo =============Made by owomushi, free to use, no need to pay for it!======================================
Echo Current Region is set to: 
%adb% shell settings get global user_settings_initialized
pause
