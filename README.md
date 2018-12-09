## Project: Linux Server Configuration
The goal of this project is to install a Linux server on Amazon Lightsail and prepare it to host my web application Catalog.

### IP Address and SSH Port
The public IP address of the server is 54.245.134.41 and the SSH port is 2200.

### URL to the web application Catalog
The complete url is:
http://54.245.134.41.xip.io/

### List of Installed Software
1. Apache HTTP Server
2. mod_wsgi
3. finger
4. git
5. virtual environment
6. The following python packages are also installed: flask, sqlalchemy, requests

### Location of SSH Public Key
1. SSH Public Key for the user "grader" is located at: /home/grader/.ssh/id_rsa
2. The passphrase to access this file is: grader

### Steps to Configure the Server
#### Get and Prepare the Server
1. Start a new Ubuntu Linux server instance on Amazon Lightsail. 
2. Connect to the server using the button "Connect using SSH" on the Lightsail instance home page.
3. After ssh to the server, update currently installed packages (sudo apt-get update, sudo apt-get upgrade).
  You may encounter a dialog asking "A new version of configuration file /etc/default/grub is available. But the version installed currently has been locally modified". If this happens, you can choose "Keep the local version installed" for now.But this will cause some packages being kept back and not upgraded. If you want to update these packages in the future, you can use the command sudo apt-get install <list of packages kept back>.
4. Set up the firewall to allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123). (sudo ufw allow 2200)
5. Add port 2200 to Amazon Firewall configuration by going to the Network tab in your Lightsail instance.
6. Download the private key from your Lightsail Account page and change its permission setting. (On your instance home page, go to "Connect" tab and scroll down to the bottom. You'll find the link to download the key).
7. Change the ssh port to 2200 by editing the file /etc/ssh/sshd_config. Locate the line # Port 22, uncomment it and change it to 2200.
8. Now you should be able to ssh to the server in your terminal using the command: ssh -i <location of your key> ubuntu@ip-address -p 2200
9. After ssh to the server, deny the connection for SSH port 22.
  
#### Prepare to Deploy the Project
1. Install Apache: sudo apt-get install apache2
2. Install mod_wsgi: sudo apt-get install libapache2-mod-wsgi.
3. Create Python virtual environment using the following steps:
'''
# To install Python’s virtual environment:
sudo apt install virtualenv
'''
