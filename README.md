For running the application, 

Creating the development environment for application
======================================================
1) Create a project directory called "virtualenv_flaskmysql" and change directory to that directory
2) Run the command "pip install virtualenv"
3) python3 -m venv "virtualenv_flaskmysql"
4) To activate the virtual environment run the command "source ./bin/activate"
5) Run the command "pip install Flask"
6) Run the command "pip install "mysql-connector-python"

Creating the database environment for application
======================================================
1) Install mysql 8 version along with mysql workbench
2) Create a schema called "bank" in through mysql workbench
3) Run the scripts present in the current folder named "table_creation.sql"
4) All tables needed for the applications will be created


Running the application
===============================
1) Copy the app.py file into the virtual environment folder called "virtualenv_flaskmysql" 
2) Type the command "python app.py"
3) The application should be running under the default port of 5000
4) Run the commands from the file "CommandsforRunningApplication" in the same order as in the file
