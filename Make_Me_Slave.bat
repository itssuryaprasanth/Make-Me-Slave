@setlocal enableextensions
@cd /d "%~dp0"
@echo off
Title Making Slave
set PYTHONPATH= %PYTHONPATH%;%cd%
cmd.exe /c pip install -r requirements.txt

echo *********** checking automation server network reachability from current network **************
python utilties/check_network.py %~4
if %ERRORLEVEL% == 1 (
	call:Stop
) else (
	call:Installation %~1 %~2 %~3 %~4 %~5
)
: Stop
echo "PLEASE CONNECT YOUR NETWORK to 100.105.2x.x  SERIES "
goto :eof

: Installation
echo ************ Pre check on operating systems ***********
python preinstallers/oschecks.py
echo *********** Creating firewall rule to ssh connection vice versa *************
call preinstallers/add_ssh_firewall_rule.bat.bat
echo *********** Installing ssh server and ssh client ******************
call preinstallers/install_open_ssh_server.bat
echo *********** Starting ssh service ******************
call preinstallers/start_ssh_service.bat
echo *********** Creating local user ********************
call preinstallers/local_user_creation.bat %1 %2
echo ********* Generating ssh keys and sending to automation server ********
python sshkeygen_generator/sshkeygen.py %4
echo ********** Creating Slave in master jenkins ***************
python jenkinshelpers/master_slave.py %5 %1 %2 %3
pause
exit /b