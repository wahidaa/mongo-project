from flask import Flask
from flask_session import Session
from datetime import timedelta
from main.config import config_by_name
def create_app(config_name):
    app = Flask(__name__,template_folder='templates')
    app.config.from_object(config_by_name[config_name])
    #app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    #app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
    # sess = Session()
    # sess.init_app(app)
    return app