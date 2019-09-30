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
3. After ssh to the server, update currently installed packages
```
sudo apt-get update
sudo apt-get upgrade
```
  You may encounter a dialog asking "A new version of configuration file /etc/default/grub is available. But the version installed currently has been locally modified". If this happens, you can choose "Keep the local version installed" for now.But this will cause some packages being kept back and not upgraded. If you want to update these packages in the future, you can use the following command
```
sudo apt-get install <list of packages kept back>
```
4. Set up the firewall to allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123). 
```
sudo ufw allow 2200
```
5. Add port 2200 to Amazon Firewall configuration by going to the Network tab in your Lightsail instance.
6. Download the private key from your Lightsail Account page and change its permission setting. (On your instance home page, go to "Connect" tab and scroll down to the bottom. You'll find the link to download the key).
7. Change the ssh port to 2200 by editing the file /etc/ssh/sshd_config. Locate the line # Port 22, uncomment it and change it to 2200.
8. Now you should be able to ssh to the server in your terminal using the command
``` 
ssh -i <location of your key> ubuntu@ip-address -p 2200
```
9. After ssh to the server, deny the connection for SSH port 22.
  
#### Prepare to Deploy the Project
10. Install Apache
```
sudo apt-get install apache2
```
11. Install mod_wsgi
``` 
sudo apt-get install libapache2-mod-wsgi
```
12. Create Python virtual environment using the following steps:
```
# To install Python’s virtual environment:
sudo apt install virtualenv
# Create New Directory in Home
cd
mkdir python-environments
cd python-environments
# Create a Virtual Environment in Python
virtualenv -p python env
# Activate Environment
source env/bin/activate
```
13. In the virtual environment, install the following python packages:flask, sqlalchemy, requests

#### Deploy the Item Catalog project
14. In the Home directory of the ubuntu user, git clone the repository for the project Catalog.
15. Create the /var/www/html/myapp.wsgi file
```
sudo nano /var/www/html/myapp.wsgi
```
16. Add the following lines in the /var/www/html/myapp.wsgi file:
```
activate_this = '/home/ubuntu/Catalog/.env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/home/ubuntu/Catalog')

from catalog_project import app as application
```
17. You need to use the asbolute URI for the database in the Catalog project. If not, update the create_engine function in catalog_project.py and database_setup.py to the following:
```
engine = create_engine(
   'sqlite:////absolute/path/to/file/catalog.db',
    connect_args={'check_same_thread': False},
)
```
18. Now the web application should be served correctly on the server.

### Reference Recoures 
1. Deploy Flask application to a WSGI server
http://flask.pocoo.org/docs/1.0/deploying/
http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/
2. Create Python Virtual Environment on Ubuntu
https://www.linode.com/docs/development/python/create-a-python-virtualenv-on-ubuntu-1610/
3. Solution to the error "(OperationalError) unable to open database file None None"
https://stackoverflow.com/questions/18208492/sqlalchemy-exc-operationalerror-operationalerror-unable-to-open-database-file
4. Solution to the update problem "The following packages have been kept back"
https://askubuntu.com/questions/601/the-following-packages-have-been-kept-back-why-and-how-do-i-solve-it
