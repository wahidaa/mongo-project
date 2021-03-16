from flask import Blueprint,g,session
from main.services.client_service import *
from decorator import required_login
from utilities import *
from flask_socketio import SocketIO, emit

client=Blueprint('client',__name__)



@client.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None

@client.before_request
def current_col_():
  if 'db' in session:
    dbs=session['db']
    g.current_col=current_col(dbs)
  else:
    g.current_col=None

@client.route('/home',methods=['POST','GET'])
def signup_logins():
    return signup_login()

@client.route('/logout',methods=['POST','GET'])
@required_login
def logouts():
    return logout()


@client.errorhandler(422)
def unprocessable(error):
    return error_422(error)

@client.errorhandler(400)
def bad_request(error):
    return error_400(error)
      
@client.errorhandler(404)
def not_found(error):
    return error_404(error)
