--INSTALLATION

#Use this command to build foundation dependencies and compile scss
git clone --depth 1  https://github.com/zurb/foundation-sites-template static
npm install
bower install
npm start

--PROJECT

Set the below environmental variables in the /etc/environment file

Flask Secret

This project uses cookie based sessions to track the author's login. You will nee to set an environmental variable in
 your host server for BLOG_SECRET_STRING

You can create a secret key using python

>>> import os
>>> os.urandom(24)

Database

You will need to set a environmental variable in your host server for the db connection string using
 BLOG_DB_CONFIG_STRING


