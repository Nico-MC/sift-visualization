# Manage pip dependencies

Generate a requirements file and then install from it in another environment.
> pip3 freeze > requirements.txt <br>
  pip3 install -r requirements.txt (but better use current requirements.txt of the repository)

Delete all .pyc files
> find . -name \\\*.pyc -delete
