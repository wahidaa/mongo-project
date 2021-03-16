from flask import Blueprint,g,session,Flask,render_template
from main.services.databaseinfo_service import *
from decorator import *
from utilities import *


databaseinfo=Blueprint('databaseinfo',__name__)

@databaseinfo.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None
@databaseinfo.before_request
def recent_connect_():
  if 'user' in session:
    id=session['user']
    g.current_connect=current_connect(id)
  else:
    g.current_user=None

@databaseinfo.before_request
def current_col_():
  if 'db' in session:
    dbs=session['db']
    g.current_col=current_col(dbs)
  else:
    g.current_col=None



@databaseinfo.route('/connect_to_db',methods=['POST','GET'])
#@required_manager
def connect_to_dbs():
    return connect_to_db()
@databaseinfo.route('/connect_to_db/<database_host>:<database_port>',methods=['POST','GET'])
def recent_connections(database_host,database_port):
    return recent_connection(database_host,database_port)

@databaseinfo.route('/db_list',methods=['POST','GET'])
def db_lists():
    return db_list()

@databaseinfo.route('/create_database',methods=['POST','GET'])
def create_new_databases():
    return create_new_database()

@databaseinfo.route('/<key>/delete_database',methods=['POST','GET'])
def delete_databases(key):
    return delete_database(key)


@databaseinfo.route('/logout_db',methods=['POST','GET'])
def db_logouts():
  return db_logout()

@databaseinfo.errorhandler(422)
def unprocessable(error):
    return error_422(error)

@databaseinfo.errorhandler(400)
def bad_request(error):
    return error_400(error)
   
@databaseinfo.errorhandler(404)
def not_found(error):
    return error_404(error)