

# """The edge_setup_step_server.sh script is a server setup script, typically used for installing and configuring server software. """


#!/bin/bash

# Script to set up ThingsBoard Edge Server
# This script includes advanced error handling and additional setup methods

LOG_FILE="/var/log/edge_setup.log"
THINGSBOARD_HOST="167.172.189.151"
ROOT_DIR="/root/PipeLineFolder"
EDGE_CODE_DIR="${ROOT_DIR}/edge_initial_code"
SSH_PASS='78WDQEuz'
TB_EDGE_SERVICE="/etc/tb-edge/conf/tb-edge.conf"

# Function to log a message
log() {
    echo "$(date) : $1" | tee -a $LOG_FILE
}

# Function to handle errors
error_exit() {
    log "$1"
    exit 1
}

# Function to update ThingsBoard configuration
update_config() {
    log "Updating ThingsBoard Edge configuration"
    rsync -va "${EDGE_CODE_DIR}/tb-edge.deb" "${EDGE_CODE_DIR}/"
    rsync -va "${EDGE_CODE_DIR}/tb-edge.conf" $TB_EDGE_SERVICE || error_exit "Error updating configuration"
}

# Function to install dependencies
install_dependencies() {
    log "Installing dependencies"
    sudo apt-get update || error_exit "Error updating package list"
    sudo apt-get install -y git sshpass || error_exit "Error installing dependencies"
}

# Function to clone or update edge_initial_code repository
update_code() {
    if [ ! -d $EDGE_CODE_DIR ]; then
        mkdir -p $EDGE_CODE_DIR
        git clone https://gitlab.appunik-team.com/Appunik_Akshay/edge_initial_code.git $EDGE_CODE_DIR || error_exit "Error cloning repository"
    else
        cd $EDGE_CODE_DIR
        git pull origin main || error_exit "Error pulling latest code"
    fi
}

# Function to install ThingsBoard Edge
install_edge() {
    log "Installing ThingsBoard Edge"
    sudo apt-get install -y maven || error_exit "Error installing Maven"
    mvn clean install -DskipTests -Ddockerfile.skip=true || error_exit "Error building ThingsBoard Edge"
    log "Setup Done"
    cd ..
    update_config
    sudo dpkg -i "${EDGE_CODE_DIR}/tb-edge.deb" || error_exit "Error installing ThingsBoard Edge package"
    sudo service tb-edge restart || error_exit "Error restarting ThingsBoard Edge service"
}

# Main installation routine
install_dependencies
update_code
install_edge
log "ThingsBoard Edge setup completed successfully"


# """This script assumes you are running as the root user or a user with sufficient privileges to install software and write to /var/log/edge_setup.log. 
# It includes functions for logging, error handling, updating the ThingsBoard Edge configuration, installing dependencies, updating code from a Git repository, and installing the ThingsBoard Edge.
# To ensure this script works as expected, you'll need to adjust the variables and repository URLs to match your environment and configuration. 
# You would save this script as edge_setup_step_server.sh and run it on the server where you want to install ThingsBoard Edge.
# Make sure to give executable permissions to this script by running chmod +x edge_setup_step_server.sh before executing it."""