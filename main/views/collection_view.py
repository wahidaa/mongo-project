from flask import Blueprint,g,session
from main.services.collection_service import *
from utilities import *
from decorator import required_login,ajax
collection=Blueprint('collection',__name__)

@collection.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None

@collection.before_request
def current_col_():
  if 'db' in session:
    dbs=session['db']
    g.current_col=current_col(dbs)
  else:
    g.current_col=None


@collection.route('/manage_collection',methods=['POST','GET'])
@required_login
def manage_collections():
    return manage_collection()
@collection.route('/manage_collection/<key>/<i>',methods=['POST','GET'])
@required_login
def get_ones(key,i):
    return get_one_collection(key,i)
def hjhj():
    print('hello')
    dicts = session['db']
    client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
    db=client[session['col']['database_name']]
    col = get_one_col(db,session['col']['col_name'])
    creat_json(col)
@collection.route('/manage_collection/<database_name>/<col_name>/filter',methods=['POST','GET'])
@required_login
def filters(database_name,col_name):   
    return filter_collection(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/filters',methods=['POST','GET'])
@required_login
def filter_collection_results(database_name,col_name):   
    return filter_collection_result(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/filter_',methods=['POST','GET'])
@required_login
def filters_(database_name,col_name):   
    return filter_collection_by_id(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/filters_',methods=['POST','GET'])
@required_login
def filter_collection_results_(database_name,col_name):   
    return filter_collection_by_id_result(database_name,col_name)


@collection.route('/manage_collection/<database_name>/<col_name>/comaparison',methods=['POST','GET'])
@required_login
def filter_comparisons(database_name,col_name):   
    return filter_comparison(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/comaparisons',methods=['POST','GET'])
@required_login
def filter_comparison_collection_results(database_name,col_name):   
    return filter_comparison_collection_result(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/logical',methods=['POST','GET'])
@required_login
def filter_logicals(database_name,col_name):   
    return filter_logical(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/logicals',methods=['POST','GET'])
@required_login
def filter_logical_collection_results(database_name,col_name):   
    return filter_logical_collection_result(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/regular',methods=['POST','GET'])
@required_login
def filter_regulars(database_name,col_name):   
    return filter_regular(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/regulars',methods=['POST','GET'])
@required_login
def filter_regular_collection_results(database_name,col_name):   
    return filter_regular_collection_result(database_name,col_name)
    
@collection.route('/manage_collection/<database_name>/<col_name>/agregate',methods=['POST','GET'])
@required_login
def agregates(database_name,col_name):
    return agregate_collection(database_name,col_name)
@collection.route('/manage_collection/<database_name>/<col_name>/agregates',methods=['POST','GET'])
@required_login
def agregate_collection_results(database_name,col_name):
    return agregate_collection_result(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/delete',methods=['POST','GET'])
@required_login
def deletes(database_name,col_name):
    return delete_collection(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/update_many',methods=['POST','GET'])
@required_login
def update_many_collections(database_name,col_name):
    return update_many_collection(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/update_many_',methods=['POST','GET'])
@required_login
def update_mn_collection_results(database_name,col_name):
    return update_mn_collection_result(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/<id>/update_one',methods=['POST','GET'])
@required_login
def updates(database_name,col_name,id):
    return update_collection(database_name,col_name,id)




@collection.route('/manage_collection/<database_name>/<col_name>/insert',methods=['POST','GET'])
@required_login
def inserts(database_name,col_name):
    return insert_collection(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/inserts',methods=['POST','GET'])
@required_login
def insert_collection_results(database_name,col_name):
    return insert_collection_result(database_name,col_name)
@collection.route('/manage_collection/<database_name>/<col_name>/inserts_',methods=['POST','GET'])
@required_login
def insert_collection_results_(database_name,col_name):
    return insert_collection_result_(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/insert_many',methods=['POST','GET'])
@required_login
def inserts_collection(database_name,col_name):
    return insert_mn_collection(database_name,col_name)



@collection.route('/manage_collection/<database_name>/<col_name>/insert_many_',methods=['POST','GET'])
@required_login
def insert_mn_collection_results(database_name,col_name):
    return insert_mn_collection_result(database_name,col_name)


@collection.route('/manage_collection/<database_name>/<col_name>/insert_file',methods=['POST','GET'])
@required_login
def insert_files(database_name,col_name):
    return insert_file(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/export_file',methods=['POST','GET'])
@required_login
def export_files(database_name,col_name):
    return export_file(database_name,col_name)

@collection.route('/manage_collection/export_file_json',methods=['POST','GET'])
@required_login
def export_file_jsons():
    return export_file_json()

@collection.route('/manage_collection/<database_name>/<col_name>/rename',methods=['POST','GET'])
@required_login
def renames(database_name,col_name):
    return rename_collection(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/<id>/delete_one',methods=['POST','GET'])
@required_login
def delete_one_documents(database_name,col_name,id):
    return delete_one_document(database_name,col_name,id)

@collection.route('/manage_collection/<database_name>/<col_name>/delete_many',methods=['POST','GET'])
@required_login
def delete_many_documents(database_name,col_name):
    return delete_many_document(database_name,col_name)

@collection.route('/manage_collection/<database_name>/<col_name>/delete_many_',methods=['POST','GET'])
@required_login
def delete_mn_document_results(database_name,col_name):
    return delete_mn_document_result(database_name,col_name)



@collection.route('/manage_collection//<key>/<i>/delete_col',methods=['POST','GET'])
@required_login
def delete_collections(key,i):
    return delete_collection(key,i)

@collection.route('/manage_collection/<key>/create_col',methods=['POST','GET'])
@required_login
def create_new_collections(key):
    return create_new_collection(key)


@collection.route('/<database_name>/collection_list',methods=['POST','GET'])
@required_login
def get_all_collections(database_name):
    return get_all_collection(database_name)




@collection.errorhandler(422)
def unprocessable(error):
    return error_422(error)
@collection.errorhandler(400)
def bad_request(error):
    return error_400(error)
@collection.errorhandler(404)
def not_found(error):
    return error_404(error)