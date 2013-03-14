# Flask Project Template
A simple flask project template with Bootstrap and tools for TDD. Useful for getting
small projects off the ground in little time.

## How to use this template 

- Create your virtualenv
- `$ git clone https://github.com/sloria/flask-template`
- Rename the folder to your project name.
- `$ cd projectname`
- Optional: Open requirements/prod.txt and specify your ORM
- Optional: Open requirements/dev.txt and specify your databases adapter
- `$ pip install -r requirements/dev.txt`
- `$ python app.py`

## Testing 
This template includes the following tools for testing:

- nose
- rednose
- watchdog
- Webtest

### Running tests
- Run tests using  `$ fab test`
- To enter "watch" mode,  `$ fab watchmedo`

## Coffeescript support 
- Run `$ fab coffee`
- Write your Coffeescript in static/coffee
- That's it!
