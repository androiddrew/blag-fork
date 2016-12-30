#Blag-fork

Blag-fork is a blogging engine written in Python using the Flask web framework, and Zurb foundation. It is intended to be simple blog engine that one can self host and feel good that they aren't using a PHP based application like Wordpress.

**Sorry Legacy python is not supported.** We make no guarantees that this software will run using a Python 2.x interpreter

##INSTALLATION

It is recommended that you create a virtual environment for running this project. Please use venv. For more info see https://docs.python.org/3/library/venv.html

Change directories into `/blag-fork` and run `pip install -r requirements.txt` to install the necessary dependencies. Please be sure to also `pip install` the appropriate DBAPI package for your RDBMS. I recommend Postgres for your backend database using psycopg2 as you DBAPI adapter.

Next you will need to change directories to `/blag-fork/blagging/static` and use these commands to build Foundation's dependencies and compile the scss. You will need to have node, npm, and bower installed globally:

```
npm install
bower install
npm start
```

This project provides a Flask-Script manager at `/blag-fork/manage.py`. Please see the documentation at https://flask-script.readthedocs.io/en/latest/


##ENVIRONMENTAL VARIABLES

Depending on the wsgi web server you choose you may need to either add the below environment variables either in the
`/etc/environment` file or pass theses as environmental variable arguments to the web server config string

###FLASK SECRET

This project uses cookie based sessions to track the author's login. You will need to set an environmental variable for BLOG_SECRET_STRING. See /blag-fork/blagging/config.py.

You can create a secret key using in the python RPEL with the below commands
```
>>> import os
>>> os.urandom(24)
```

Be sure to escape any `\` in the output when passing this string to a wsgi web server's config

###DATABASE CONNECTION STRING

This project uses SQLAlchemy. You will need to set a environmental variable for the db connection string using BLOG_DB_CONFIG_STRING. Database connections strings are dependent on the database you choose for the backend see http://docs.sqlalchemy.org/en/latest/core/engines.html for details relating to your specific server.


##WSGI SERVERS

###GUNICORN

If you are not famaliar with WSGI servers it is recommended that you start with gunicorn. To serve this in production in a modern Linux distro you will want to create a systemd unit file that executes the wsgi app. Here is an example config that can help boot strap your project. You will want to change these parameters as needed, and you can find all the documentation at http://docs.gunicorn.org/en/stable/index.html:
```
    gunicorn --reload --workers 3 --log-syslog --bind [your bind] --env BLOG_SECRET_STRING=[your secret string] --env BLOG_DB_CONFIG_STRING=[your sqlachemy string] -m 007 blog_wsgi:app
```

Digital Ocean has an excellent article for serving Flask Web Applications behind Nginx. I recommend reading the following for those who's WSGI foo is wanting https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04

##HELPER CODE

Use the below command after changing your .service file for this software. Trust me it helps a lot
```
    sudo systemctl daemon-reload && sudo systemctl restart blag-fork && sudo systemctl status blag-fork
```


