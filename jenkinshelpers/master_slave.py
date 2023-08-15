import os
import re
import subprocess
import sys
import time
import jenkins
import uuid
import yaml
from jenkinsapi.jenkins import Jenkins as jencred
from jenkinsapi.credential import UsernamePasswordCredential
from utilties.customlogger import file_logger

log = file_logger()

user_inputs = [_input for _input in sys.argv]

path_to_yaml_file = f"{os.getcwd()}//sshkeygen_generator//credentials.yaml"
with open(path_to_yaml_file) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    user_data = data['JENKINS']


class AddSlaveToMaster:

    def __init__(self):
        self.creds = None
        self.id = None
        self.cred_instance = None
        self.sut_name = None
        self.server = None
        self.jenkins_url = user_inputs[1]
        self.jenkins_username = user_data["JENKINS_USERNAME"]
        self.jenkins_password = user_data["JENKINS_PASSWORD"]
        self.cred = None
        self.slave_user_name = user_inputs[2]
        self.slave_user_password = user_inputs[3]
        self.slave_ip = user_inputs[4]

    def login_into_jenkins(self) -> None:
        """
         Login into jenkins with jenkins url, jenkins username , jenkins password and
         will wait until jenkins server is online
        :return: None
        """
        log.debug("Login into jenkins server")
        try:
            self.server = jenkins.Jenkins(self.jenkins_url, username=self.jenkins_username,
                                          password=self.jenkins_password)
            if self.server.wait_for_normal_op(30):
                log.info("Login Successfully")
                print('JENKINS SERVER IS UP & RUNNING')
            else:
                log.debug("Login Failed")
                print('UNABLE TO CONNECT TO JENKINS SERVER')
        except Exception as e:
            log.debug("Error, Login to jenkins failed {}".format(e))
            raise Exception("Error, Login to jenkins failed")

    def jenkins_user_and_version(self) -> None:
        """
         To Check Who as login into jenkins server and will also
         get the version
        :return: None
        """
        self.login_into_jenkins()
        self.server.get_whoami()
        self.server.get_version()

    def get_sut_model_name(self) -> None:
        """
         We will get current system model name
         and will use as Slave label
        :return: None
        """
        log.debug("Getting Sut Name")
        cmd = "systeminfo".split(' ')
        try:
            output = subprocess.check_output(cmd).decode().strip()
            lines = output.split("\n")
            sut_name_regex = str(str(lines[12]).strip()).replace('System Model', '')
            self.sut_name = re.search('^:\W+(.*)', sut_name_regex).group(1)
            log.info("Sut name ---> {}".format(self.sut_name))
        except Exception as e:
            log.debug("Getting sut model name failed {}".format(e))
            raise Exception("Error, Getting sut model name failed")

    def create_user_name_password_credentials(self):
        """
        Creating user_name and password in jenkins credentials
        manager, User can use in nodes or in trigger
        :return: f8be08ae-b8ab-48d2-aaef-be54d955e2f8 --> format
        """
        log.debug("Creating user name and password credientals")
        try:
            self.cred_instance = jencred(self.jenkins_url, username=self.jenkins_username,
                                         password=self.jenkins_password)
            self.id = uuid.uuid4()
            self.creds = self.cred_instance.credentials
            creds_description1 = f'{self.sut_name}' + f'{self.id}'

            cred_dict = {
                'description': creds_description1,
                'userName': f'{self.slave_user_name}',
                'password': f'{self.slave_user_password}'
            }
            self.creds[creds_description1] = UsernamePasswordCredential(cred_dict)
            log.info("Credentials created under jenkins credentials")
            return list(self.creds.credentials.keys())[-1]
        except Exception as e:
            log.debug("Credentials creation failed with an error {}".format(e))
            raise Exception("Error, Credentials creation failed")

    def create_slave_node_in_jenkins(self) -> None:
        """
         Create agent in jenkins with SSH Connection Launcher
        :return: None
        """
        log.debug("Creating slave node architecture in master jenkins")
        try:
            user_cred = self.create_user_name_password_credentials()

            if self.server.node_exists(name=self.sut_name):
                log.info("Sut is already a slave in master jenkins")
                print("YOUR SUT IS ALREADY A SLAVE IN MASTER JENKINS")
                log.info("Deleting the existing node , creating a new node")
                print("DELETING THE EXISTING NODE , CREATING A NEW NODE")
                self.server.delete_node(name=self.sut_name)

            params = {
                'host': f'{self.slave_ip}',
                'port': '22',
                'credentialsId': user_cred
            }
            log.debug("parameters for creating node {}".format(params))
            self.server.create_node(name=f'{self.sut_name}', numExecutors=2,
                                    nodeDescription=f'{self.sut_name} SLAVE', remoteFS='C:/Jenkins_Slave', labels='SLAVE 1',
                                    exclusive=False, launcher=jenkins.LAUNCHER_SSH, launcher_params=params)
            print("WAIT UNTIL AGENT COMES TO ONLINE")
            log.debug("Wait until agent comes to online")
            time.sleep(20)
            node_status = self.server.get_node_info(name=self.sut_name)
            if node_status['offline']:
                print("YOUR SUT IS OFFLINE")
                log.debug("Agent is offline")
            else:
                print("YOUR SUT IS ONLINE AND READY FOR EXECUTION")
                log.info("Agent is online")
        except Exception as e:
            log.debug("Creating slave node in jenkins failed {}".format(e))
            raise Exception("Failed, Creating slave node in jenkins")


if __name__ == '__main__':
    obj = AddSlaveToMaster()
    obj.login_into_jenkins()
    obj.get_sut_model_name()
    obj.create_slave_node_in_jenkins()
