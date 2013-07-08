# Flask Project Template
A simple flask project template with Bootstrap, a full testing suite, Peewee ORM, and Coffeescript support.
 
Loosely based of [this Django project template](https://github.com/sloria/django-base-template).

## How to use this template 

- Create your virtualenv
- `git clone https://github.com/sloria/flask-template PROJECTNAME`
- Rename the folder to your project name.
- `cd PROJECTNAME`
- `pip install -r requirements/dev.txt`
- `python run.py`

Features:

Class-based views:
- [Flask-Classy](http://pythonhosted.org/Flask-Classy/)

ORM:

- [Peewee](http://peewee.readthedocs.org/en/latest/)
- [flask-peewee](http://flask-peewee.readthedocs.org/en/latest/)
    - Also provides admin, authentication, REST API

Testing:

- nose
- watchdog
- Webtest

Deployment:
- gunicorn

### Running tests
- Run tests using  `fab test`
- To enter "watch" mode,  `fab watchmedo`

## Coffeescript support 
- Run `fab coffee`
- Write your Coffeescript in project/static/coffee
- That's it!

## License
Licensed under the MIT license. See the bundled LICENSE file for more details.
