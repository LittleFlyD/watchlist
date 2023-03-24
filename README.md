# watchlist web appplication

This is a learning practice, learned from https://github.com/helloflask/watchlist, to develop a flask web application from the very begining:
 - from init python project, init virtual env, init git 
 - to build the aplication step by step: 
    - the app module, static, template, database, form, login management
    - the unittest and test coverage
    - the project structure enhancement
 - to finally deploy to a remote server: http://hiroo.pythonanywhere.com/index 
 
 ![Screenshot](watchlist_app/static/images/watchlist-app.png?raw=true)
 
## Project Structure
```
├── requirements.txt
├── test_watchlist.py
├── watchlist_app
│   ├── __init__.py     # init app
│   ├── commands.py     # db scripts
│   ├── errors.py       # error handling api
│   ├── forms.py        # flask-wtk form
│   ├── models.py       # db models
│   ├── static
│   │   ├── images
│   │   └── style.css
│   ├── templates       # html templates
│   └── views.py        # common api routers
└── wsgi.py
```

## Installation And Running
```shell
# clone project
git clone https://github.com/LittleFlyD/watchlist.git

# create virtual env 
# skip..., can refer https://tutorial.helloflask.com/ready/#_4 

# install packages
pip install -r requirements

# forge fake db data
flask forge

# create app user
flask admin
# this cmd will help you to create a user to login the app, cmd output will be like below...
#(.venv)% flask admin
#Username: hiro
#Password: 
#Repeat for confirmation: 
#Updating user...
#Done.


# run app
flask run
* Running on http://127.0.0.1:5000/
```
