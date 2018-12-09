# Project: Catalog
This project developing an application that provides a list of gears within a variety of sports, as well as provide a user registration and authentication system.

# About the Database
There are 3 tables in the news database: Category, Item, User.

1. "Category" table: Consists of the list of sport categories. Each row has two columns: id (primary key) and name which is the name of the sport. 

2. "Item" table: Includes information about all the sport gears. Each row has 6 columns: id (primary key), name, time_added, description, user_id, and category_name. "user_id" is a foreign key that relates to the id column in User table and category_name is also a foreign key that relates to the name column of Category table. "time_added" will be populated by the acutal time when the item is created/added, and it will be updated when the item is editted. 

3. "User" table: Consists of the information about the users registered in the application. Each row has 3 columns: id (primay key), name and email. Since this application only implements authentication via Google,the "email" will be user's gmail account and "name" will be the name associated with that account.

# Configuration
1. This project requires the use of virtual machine. You can download it here https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
2. Download and install Vagrant from https://www.vagrantup.com/downloads.html
3. Download the Vagrant configuration from this repository https://github.com/udacity/fullstack-nanodegree-vm . Unzip the downloaded file and cd into the vagrant directory inside it. 
4. Then use "vagrant up" in the terminal to bring the vm up. And use "vagrant ssh" to log into the vm. 

# Download Project Files
1. Please download the zip file Catalog_YL.zip and unzip it.
2. Put the folder into the vagrant directory.
3. Please run the file lots_of_data.py first. This will create some data so that the rendered page won't be blank. 
4. The file catalogProject.py consists of the source code to run the server. The file database_setup.py contains the code to set up the database models. The information needed to use Google OAuth is saved in client_secrets.json. 

# Run the Code
1. Please make sure to complete the steps in the section "Configuration and Data" and "Download Project Files"
2. cd to the vagrant directory and then cd to the directory Catalog_YL.
3. Please run lots_of_data.py first by typing the following command into terminal: ./lots_of_data.py
4. Then run the server by typing the following command into terminal: ./catalog_project.py
5. Now you'll be albe to access the pages listed in Availalbe URLs.

# Available URLs
The application is hosted on localhost://8000 and it implements the following URLs:
1. localhost://8000
    Returns all the sport categories and the latest 9 items added to the database. 
    Without signing in, this page will render the html template "all_categories_not_loggedin.html". And on the page, there won't be a button to add new items.
    With signing in, the page will render the html template "all_categories_loggedin.html" instead and shows an "Add Item" button. 
2. localhost://8000/catalog/<string:category_name>/items
    Returns the gears/equipments within a certain sport category.
3. localhost://8000/catalog/add
    Returns the page to add a new item. This page can only be accessed when the user is signed in and is the owner of that item.
4. localhost://8000/catalog/<string:category_name>/<string:item_name>
    Returns a page with description of an item.
    When logged in, this page will also show the button to edit or delete an item.
5. localhost://8000//catalog/<string:item_name>/edit
    Returns the page to edit an item. This page can only be accessed when the user is signed in and is the owner of that item.
6. localhost://8000//catalog/<string:item_name>/delete
    Returns the page to delete an item. This page can only be accessed when the user is signed in and is the owner of that item.
