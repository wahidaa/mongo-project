from flask import Blueprint,g,session
from main.services.administrator_service import *
from decorator import *
from utilities import current_user


administrator=Blueprint('administrator',__name__)


@administrator.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None

@administrator.before_request
def current_col_():
  if 'db' in session:
    dbs=session['db']
    g.current_col=current_col(dbs)
  else:
    g.current_col=None


@administrator.route('/all_clients',methods=['POST','GET'])
@required_login
@required_manager
def get_all_clientss():
    return get_all_clients()

@administrator.route('/users',methods=['POST','GET'])
@required_login
@required_manager
def get_all_userss():
    return get_all_users()


@administrator.route('/administrators',methods=['POST','GET'])
@required_login
@required_manager
def get_all_administratorss():
    return get_all_administrators()

@administrator.route('/add_user',methods=['POST','GET'])
@required_login
@required_manager
def add_users():
    return add_user()

