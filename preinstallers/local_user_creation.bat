@setlocal enableextensions
@cd /d "%~dp0"
@echo off
net user %1 %2
WMIC USERACCOUNT WHERE "Name='%1'" SET PasswordExpires=FALSE
WMIC USERACCOUNT WHERE "Name='%1'" SET Passwordchangeable=FALSE
net localgroup administrators "%1" /add