@setlocal enableextensions
@cd /d "%~dp0"
@echo off
echo Creating Inbound Rule In Windows Defender Rule
powershell.exe -Command New-NetFirewallRule -DisplayName "SSHConnection"  -Name "SSH" -Description "SSHConnectionEstablishment" -Direction Inbound -LocalPort 22 -Protocol TCP -Action Allow