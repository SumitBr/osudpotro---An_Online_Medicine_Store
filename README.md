# pharmacy-cse470-project

## About Project
- **Models** are in `MVC/models.py`
- **Controllers** are in `MVC/controllers.py`
- **Views** are in `MVC/views/*`
- **Routes** are in `MVC/routes.py`
- **Tests** are in `MVC/tests.py`
---
## Run Project
### Install Prerequisites
- `python`
- `python-virtualenv`
    - Or, `$ pip install virtualenv`
### Download Project
- `$ git clone --depth 1 https://github.com/wasique-shafin/pharmacy-cse470-project`
### Move into Project Folder
- `$ cd pharmacy-cse470-project`
### Build Python Virtual Environment (build once only)
- `$ python -m venv env`
- `$ source env/bin/activate` for **Linux/MacOS**
- `$ env\Scripts\activate.bat` for **Windows**
- `$ pip install -r requirements.txt`
    - Or, `$ pip install django pillow six django-countries coverage`
### Activate Python Virtual Environment
- `$ source env/bin/activate` for **Linux/MacOS**
- `$ env\Scripts\activate.bat` for **Windows**
### Start Project Server
- `$ python manage.py runserver`
### Access Project Website
- Open `http://127.0.0.1:8000/` in **Browser**
 