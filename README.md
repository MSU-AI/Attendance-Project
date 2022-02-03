To run this website, first [install Django](https://docs.djangoproject.com/en/3.2/topics/install/#installing-official-release):

```
python -m pip install -r requirements.txt
```

*(Note: You MUST use python 3! I had multiple versions on my computer, so I had to replace `python` with `python3`. In certain cases, the python command may be named `py`. It will probably depend on your exact setup.)*

After the modules have been installed,
you can configure the project using these commands:

```
python manage.py migrate
python manage.py createsuperuser
```

Follow the prompts when given.

# Run the site
Once you have Django installed, open a terminal in this directory and run the following command:
```
python manage.py runserver
```

That will start the local server. Once that command is running, you will be able to view the site at http://localhost:8000/

(When you do this, your terminal is acting like a web server, and your browser is accessing that local server.)

# Sign in to the admin panel
Once the server is running, visit http://localhost:8000/admin to view the admin panel.
Sign in with the username `test` and password `test`. (You can also [create a new account](https://docs.djangoproject.com/en/3.2/intro/tutorial02/#creating-an-admin-user) from the terminal.)

# Updating the data models
If you want to change the data models which appear in the admin panel, edit them in `attendanceapp/models.py`. Then run the following two commands in order:
```
python manage.py makemigrations attendanceapp
python manage.py migrate
```

**Not appearing?** If you create any new models, you will need to update `attendanceapp/admin.py` to make them appear in the admin panel.
