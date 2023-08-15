import re
import subprocess
import sys
from utilties.customlogger import file_logger

log = file_logger()
current_windows_version = None


class OsChecks:

    def validate_windows_version(self):
        global current_windows_version
        log.info("Checking Current Running Windows Version")
        cmd = "systeminfo".split(' ')
        try:
            output = subprocess.check_output(cmd).decode('utf-8').strip()
            lines = output.split("\n")
            current_windows_version = str(lines[1]).strip()
            current_windows_version = re.search('.*Microsoft(.*)', current_windows_version).group(1).strip()
            if not current_windows_version.find('Windows 10') or current_windows_version.find(
                    'Windows 11'):
                raise WindowsError('OPERATING SHOULD BE 10 OR HIGHER')
            print(f"WINDOWS VERSION IS {current_windows_version}")
            log.info(f"Current Windows Version ---> {current_windows_version}")
        except (WindowsError, AttributeError, TypeError):
            log.error("Problem in checking windows version, please check below error message")
            log.info(sys.exc_info())
            print(f"CURRENT WINDOWS VERSION IS NOT {current_windows_version}")

    def validate_powershell_version(self):
        log.info("Checking Current Powershell Version")
        try:
            output = subprocess.run(['powershell.exe', '$PSVersionTable'], capture_output=True)
            ps_output = str(output.stdout)
            _regex = re.search('([0-9].+)', ps_output).group()
            if not int(str(_regex)[0]) >= 5:
                raise WindowsError('POWERSHELL VERSION SHOULD BE GREATER THAN 5 OR EQUAL TO 5')
            print("True")
            print(f"POWERSHELL VERSION IS {str(_regex)[0:13]}")
            log.info(f"Current Powershell Version ---> {_regex[0:13]}")
        except AttributeError as e:
            log.error("Problem in checking Powershell version, please check below error message")
            log.info(sys.exc_info())
            print(f"CURRENT POWERSHELL VERSION SHOULD BE EQ OR GT THAN --> {str(_regex)[0:13]}")

    def validate_current_account_in_administrator_group(self):
        log.info("Checking Current_User_Account_in_Administrator_Group")
        try:

            output = subprocess.run(['powershell.exe', '-Command',
                                     '(New-Object Security.Principal.WindowsPrincipal(['
                                     'Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole(['
                                     'Security.Principal.WindowsBuiltInRole]::Administrator)'],
                                    capture_output=True)
            ps_output = str(output.stdout).replace("\n", '')
            _regex = re.search('(True|False)', ps_output).group()
            if _regex.__contains__("False"):
                print("False")
            log.info(f"Current_User_Account_in_Administrator_Group ---> {_regex}")
        except TypeError:
            log.error("Problem in checking Current_User_Account_in_Administrator_Group, please check below error "
                      "message")
            log.info(sys.exc_info())


if __name__ == '__main__':
    obj = OsChecks()
    obj.validate_windows_version()
    obj.validate_powershell_version()
    obj.validate_current_account_in_administrator_group()
