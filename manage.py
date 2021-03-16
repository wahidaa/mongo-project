import os
import unittest
from flask import session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from main import  create_app
from main.views.client_view import client 
from main.views.databaseinfo_view import databaseinfo
from main.views.collection_view import collection
from main.views.administrator_view import administrator
app = create_app(os.getenv('SERVICE_ENV') or 'dev')
app.register_blueprint(client)
app.register_blueprint(databaseinfo)
app.register_blueprint(collection)
app.register_blueprint(administrator)
app.app_context().push()
manager = Manager(app)
@manager.command
def run():
    
    app.run()
   


@manager.command
def test():

    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('tests/unittest', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
   
