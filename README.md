# Make-Me-Slave
# Jenkins Slave Setup and Regression Test Execution Script

This script facilitates the seamless addition of a System Under Test (SUT) as a Jenkins slave  With a combination of API calls and automation, you can effortlessly integrate new SUTs into your Jenkins environment and run regression tests without manual intervention.

## Features

- **Automated Jenkins Slave Setup**: This script uses Jenkins API calls to dynamically add the SUT as a Jenkins slave, enabling it to be managed by the Jenkins master.
- **SUT Integration Made Easy**: Say goodbye to manual configuration. The script streamlines the entire process, reducing the chances of errors and saving time.

## Prerequisites

- Jenkins Master URL, Jenkins System IP
- SUT Configuration Details (IP)

## Usage

1. Clone this repository to your local machine or directly onto your Jenkins server.

2. Navigate to the repository directory:

   ```bash
   cd sshkeygen_generator
   ```

3. Edit the `credientals.yaml` file with your Jenkins System IP, Username, Password.

4. Run the script with arguments:

5. Arguments: Local Username, Local Password, Local System IP Jenkins System IP, Jenkins Master URL

   ```bash
   Make_Me_Slave.bat 
   ```

6. The script will initiate the following steps:
   - Authenticate with the Jenkins master using the provided Password.
   - Create a new Jenkins node (slave) for the SUT.


## Contributions

Contributions are welcome! If you encounter issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

By using the Jenkins Slave Setup and Regression Test Execution Script, you can effortlessly integrate new SUTs into your Jenkins environment and initiate regression tests with a single command. Say hello to streamlined automation and enhanced testing efficiency!
