import os
import subprocess
import paramiko
import yaml
from utilties.customlogger import file_logger
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

log = file_logger()

path_to_yaml_file = os.getcwd()+"\\sshkeygen_generator\\"+"credentials.yaml"
with open(path_to_yaml_file) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    user_data = data['JENKINS']


def generate_keys():
    log.debug("Generating ssh keys")
    try:
        if not os.path.exists(f"{os.getenv('USERPROFILE')}\\.ssh"):
            log.debug(".ssh folder doesn't exists, creating new")
            os.mkdir(f"{os.getenv('USERPROFILE')}\\.ssh")
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.TraditionalOpenSSL,
            crypto_serialization.NoEncryption()
        )
        file_out = open(f"{os.getenv('USERPROFILE')}\\.ssh\\private", "wb")
        file_out.write(private_key)
        file_out.close()
        log.info("Private key is generated")
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )
        file_out = open(f"{os.getenv('USERPROFILE')}\\.ssh\\public.pub", "wb")
        file_out.write(public_key)
        file_out.close()
        log.info("Public key is generated")
    except Exception as e:
        log.debug("Error, generating public/private key failed {}".format(e))
        raise Exception("Error, SSH keygen failed")


def add_private_key_to_ssh_agent():
    log.debug("Adding private key to ssh agent automatically retrieve local private key and pass to ssh client")
    try:
        cmd = "ssh-add $env:USERPROFILE\.ssh\private"
        cli_output = subprocess.run(['powershell.exe', '-Command', cmd], capture_output=True)
        if cli_output.returncode == 1:
            log.debug("Private key is not added to ssh agent identifiers")
            raise Exception("Private Key is not added to ssh agent identifiers")
        log.info("Private key is added to ssh agent")
    except Exception as e:
        log.debug("Error,adding private key to ssh agent failed {}".format(e))
        raise Exception("Error, private key to ssh agent failed")


def standard_admin_user_authorized_keys():
    log.debug("Transferring public keys to server as standard user")
    try:
        log.info("Getting content from public key and storing it a variable")
        first_cmd = 'Get-Content -Path $env:USERPROFILE\.ssh\public.pub'
        cli_output = subprocess.run(['powershell.exe', '-Command', first_cmd], capture_output=True, encoding='utf-8')
        cli_output = str(cli_output.stdout).replace('\n', '')
        log.debug("Successfully stored in a powershell variable")
        second_cmd = fr"powershell New-Item -Force -ItemType Directory -Path $env:USERPROFILE\.ssh; Add-Content -Force -Path $env:USERPROFILE\.ssh\authorized_keys -Value '{cli_output}'"
        third_cmd = fr"powershell Add-Content -Force -Path $env:ProgramData\ssh\administrators_authorized_keys -Value '{cli_output}';icacls.exe" + r"$env:ProgramData\ssh\administrators_authorized_keys"" /inheritance:r /grant ""Administrators:F"" /grant ""SYSTEM:F"
        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_connection.connect(hostname=user_data['JENKINS_SYSTEM_IP'], username=user_data['JENKINS_SYSTEM_USERNAME'],password=user_data['JENKINS_SYSTEM_PASSWORD'], port=22)
        ssh_connection.exec_command(command=second_cmd, timeout=60)
        ssh_connection.exec_command(command=third_cmd, timeout=60)
        log.info("Contents of public key are storing in authorizedkeys file")
        log.info("Successfully stored in authorizedkeys file")
        ssh_connection.close()
    except Exception as e:
        log.debug("Error, Standard, Admin user authorized keys placing failed {}".format(e))
        raise Exception("Error, Standard Admin user authorized keys placed failed")


generate_keys()
add_private_key_to_ssh_agent()
standard_admin_user_authorized_keys()
