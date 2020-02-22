This project explores basic concepts regarding Python, Relational Databases, Queries, Server Side Rendering and the Flask Framework.

# Features
- Adding/Deleting/Editing categories
- Adding/Deleting/Editing posts
- Adding/Deleting/Editing Comments
- Logging in using Google or Facebook (OAuth 2.0 authentication mechanism)
- Querying/Searching specific posts/categories
- Viewing user profiles
- Editing user BIOs/status
- JSON API Endpoints (Showing JSON serialized forms of pages)

# TODO:
- Change the architecture of the back-end to a RESTful API instead of SSR(Server Side Rendering).
- Use AJAX requests instead of using links when editing/removing/adding messages.
- Redesign the layout.

# Permissions:
## Member(user_rank = 0):
- Add/Edit/Delete posts
- Add/Edit/Delete their own comments
- Update bio/status
- Search for posts/categories


## Admin(user_rank = 1):
- *All user features +*:
- Add/Edit/Delete Categories
- Delete other users' comments


# Setup
### How to get/install Python version 2 or 3
Download link: https://www.python.org/downloads/


### How to get/install VirtualBox
Download link: https://www.virtualbox.org/wiki/Downloads


### How to get/install and setup Vagrant
*Step One* - Download and install vagrant from https://www.vagrantup.com/downloads.html

*Step Two* - Create a *_vagrant_* directory

*Step Three* - Download *Vagrantfile* from Udacity's repository 
and move it to the *_vagrant_* directory
(Link: https://github.com/udacity/fullstack-nanodegree-vm/tree/master/vagrant)

*Step Four* - ```cd``` into the *_vagrant_* directory with your shell(windows - Git Bash, Linux/Mac OS- Terminal) 

*Step Five* - run the command ```vagrant up``` with your shell in order to turn on the virtual machine
and then run ```vagrant ssh``` in order to get into the virtual machine shell 


### How to get third-party credentials

- Facebook: 
*Step One* - Enter https://developers.facebook.com/
*Step Two* - Sign into your own facebook account
*Step Three* - Add a new app
*Step Four* - In 'app domains' insert 'localhost'

Copy the app ID and insert it into /templates/login.html/  where it says
APP_ID_HERE in the facebook login button section

Insert the App ID and Client Secret into the fb_client_secrets.json that is included in the repository

- Google:
*Step One* - Enter https://console.developers.google.com/

*Step Two* - Login to your google acount

*Step Three* - Create a new project on Google's console (Select a project -> New Project)

*Step Four* - Enter the project that you created

*Step Five* - Enter into the Credentials section

*Step Six* - Click 'Create Credentials' and then 'OAuth Client ID'

*Step Seven* - In 'Authorized JavaScript origins' enter 'localhost:8000'

*Step Eight* - In 'Authorized redirect URIs' enter 		

http://localhost:8000/,	

http://localhost:8000/gconnect,	

http://localhost:8000/login

*Step Nine* - Click 'Save'

Copy the Client ID and insert it into the /templates/login.html/ where it says
CLIENT_ID_HERE in the google login button section

Click 'Download JSON', rename the downloaded file to 'client_secrets.json' and place it in the main directory of the app

### How to edit the database (for changing your rank for example)

- Download 'DB Browser for SQLite' from https://sqlitebrowser.org/

- Run it and open the database using the 'Open Database' 

In order to change/create/delete information in the database click the 'Browse Data' tab 


# How to run the project

*Step One* - Enter the vagrant folder using Git Bash (```cd DIRECTORY```)

*Step Two* - Enter into vagrant (```vagrant up``` and then ```vagrant ssh```)

*Step Three* - Enter the project folder (```cd DIRECTORY```)

*Step Four* - Run the following script ```python finalProject.py```

*Step Five* - Open your web browser and enter ```localhost:8000```
