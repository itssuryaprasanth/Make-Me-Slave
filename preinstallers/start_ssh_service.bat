@setlocal enableextensions
@cd /d "%~dp0"
@echo off
echo Starting the SSH Service ...
net start "sshd"
echo ***********************************
echo Making SSH Service To Start Automatic ...
sc config "sshd" start=auto
powershell Start-Service sshd
echo ***********************************
echo Finished ....
echo Making "ssh-agent" to start automatic..
sc config "ssh-agent" start=auto
powershell Start-Service "ssh-agent"
echo ************************************
echo Finished........