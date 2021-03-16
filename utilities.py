import pymongo
from pymongo import MongoClient
import psycopg2
import bcrypt
import pandas
from flask import session
from settings import *
# postgres functions 
def postgres_connetion(host,db_name,db_user,db_password):
    con = psycopg2.connect(" host={} dbname={} user={} password={}".format(host,db_name,db_user,db_password))
    
    print("You are connected ")
    return con

def post_resource(output,table_name,cur):
    columns = ""
    column=output.keys()    
    for i in range(len(column)):
        columns += "%s," 
    values=tuple(output.values())
    sql = f""" insert into {table_name}  values ({columns[:-1]})"""
    cur.execute(sql,values)

def post_resource_1(output,table_name,cur):
    column=output.keys()
    columns= '(%s)' % ', '.join(map(str, column))
    values=tuple(output.values())
    sql =f""" insert into {table_name} {columns} values {values}"""
    cur.execute(sql)

def patch_resource(body_request,table_name,cur,filter_criteria):
    cur.execute("select * from {} where {}='{}'".format(table_name,filter_criteria,body_request['message']['id']))
    record = cur.fetchone()
    if not  record:
        abort(404)
    liste = list(body_request['message'][table_name].keys())
    sql="update {} set ".format(table_name)
    if liste:
        for i in liste:
            sql = sql  + "{}='{}',".format(i,body_request['message'][table_name]['{}'.format(i)]) 
        cur.execute(
            sql +"updated_at='{}' , updated_by='system'".format(
                datetime.datetime.now()) +" where {}='{}'".format(
                    filter_criteria,
                    body_request['message']['id']))

def delete_resource(table_name,filter_criteria,body_request,cur):
    sql="""DELETE FROM {} WHERE {} =%s;""".format(table_name,filter_criteria)
    cur.execute(sql,(body_request['message']['account_id'],))

def get_resources_by_filter(table_name,filter_criteria,filter_criteria_value,cur):
    sql=(
        f"""select * from {table_name} where {filter_criteria}='{filter_criteria_value}'""")
    cur.execute(sql)
    record=cur.fetchall()
    return record

def get_all_resources(table_name,cur):
    sql= f"""select * from {table_name}"""
    cur.execute(sql)
    record=cur.fetchall()
    return record
    
def get_list_clients_by_type(cur,nb_page,filter_criteria):
    page_result=5
    offset=0
    offset=offset+page_result*(nb_page-1)
    psql_base=f""" select *,(
    select count(*)
    from client where user_type = '{filter_criteria}') 
    from client where user_type = '{filter_criteria}' 
    """
    psql_page=f"""ORDER BY client_id
    OFFSET {offset} ROWS
    FETCH NEXT {page_result} ROWS ONLY"""
    psql=psql_base+psql_page
    cur.execute(psql)
    record=cur.fetchall()
    count=record[0][7]
    return count,page_result,record

def get_list_clients(cur,nb_page):
    page_result=5
    offset=0
    offset=offset+page_result*(nb_page-1)
    psql_base=""" select *,(
    select count(*)
    from client ) 
    from client 
    """
    psql_page=f"""ORDER BY client_id
    OFFSET {offset} ROWS
    FETCH NEXT {page_result} ROWS ONLY"""
    psql=psql_base+psql_page
    cur.execute(psql)
    record=cur.fetchall()
    count=record[0][7]
    return count,page_result,record

def check_existence(table_name,filter_criteria,filter_criteria_value,cur):
    sql = f"select exists(select 1 from {table_name} where {filter_criteria}= '{filter_criteria_value}')"
    print(sql)
    output = cur.execute(sql)
    return output

def get_resource(column_name,table_name,filter_criteria,filter_criteria_value,cur):
    sql=(
        f"""select {column_name} from {table_name} where {filter_criteria}='{filter_criteria_value}'""")
    cur.execute(sql)
    record=cur.fetchone()
    return record

def current_user(id):
    con=postgres_connetion(
        host,
        db_name,
        db_user,
        db_password)
    cur=con.cursor()
    psql=(
    f"""select client_id,user_type,user_name from client where client_id='{id}'""")
    cur.execute(psql)
    record=cur.fetchone()
    return record

def current_connect(id):
    con=postgres_connetion(
        host,
        db_name,
        db_user,
        db_password)
    cur=con.cursor()
    psql=(
    f"""select database_host,database_port from databaseinfo where client_id='{id}'""")
    cur.execute(psql)
    record=cur.fetchall()
    return record



def hash_string(password,pepper):
    password_peppred=(str(password)+pepper).encode("utf-8")
    hashed = bcrypt.hashpw(password_peppred, bcrypt.gensalt())
    return hashed

def check_password(password,hashed,pepper):
    if bcrypt.checkpw(str(password+pepper).encode("utf-8"), hashed.tobytes()):
        return True
    else:
        return False

#mongo functions
def mongo_create_connect(database_host,database_port,maxSevSelDelay):
    client = pymongo.MongoClient(database_host,database_port, serverSelectionTimeoutMS=maxSevSelDelay)
    info = client.server_info()
    session['version'] = info['version']
    return client

def get_one(db,col_name,nb_page):
    colls=[]  
    page_result=10
    offset=0
    offset=offset+page_result*(nb_page-1)
    col = db[f"{col_name}"]
    count = col.count()
    cursors = col.find().skip(offset).limit(page_result).sort("_id", 1)
    for cursor in cursors:
        colls.append(cursor)
    return colls,count,page_result

def get_one_col(db,col_name):
    colls=[]  
    col = db[f"{col_name}"]
    cursors = col.find()
    for cursor in cursors:
        colls.append(cursor)
    return colls

def get_all_documents(db,col_name):
    colls=[] 
    col = db[f"{col_name}"]
    count = col.count()
    cursors = col.find()
    for cursor in cursors:
        colls.append(cursor)
    return colls

def download_csv(file_name):

    with open(f'csv_file/{file_name}','r') as f:
        csv_file=f.read()
    response = make_response(csv_file)
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    return response

def create_lists(colls):
    ids = []
    keys = []
    values = []
    for coll in colls:
        ids.append(coll['_id'])
        k= [key for key in coll.keys()]
        v= [key for key in coll.values()]
        keys.append(k[1:])
        values.append(v[1:])
    return ids, keys,values

def get_all(client,database_name): 
    db=client[database_name]  
    col_name = db.collection_names()
    return col_name

def fun_filters(db,col_name,query,nb_page):
    colls=[]  
    page_result=10
    offset=0
    offset=offset+page_result*(nb_page-1)
    mycol = db[f"{col_name}"]
    count = mycol.find(query).count()
    cursors = mycol.find(query)
    for cursor in cursors:
        colls.append(cursor)
    return colls,count,page_result

def fun_filters_order(db,col_name,query,field,order,nb_page):
    colls=[]  
    page_result=10
    offset=0
    offset=offset+page_result*(nb_page-1)
    mycol = db[f"{col_name}"]
    count = mycol.find(query).count()
    cursors = mycol.find(query).sort(f"{field}", order)
    for cursor in cursors:
        colls.append(cursor)
    return colls,count,page_result

def fun_filters_limit(db,col_name,query,limits,nb_page):
    colls=[]
    page_result=10
    if limits < page_result: 
        page_result = limits 
        
    else:
        page_result=page_result
    offset=0
    offset=offset+page_result*(nb_page-1)
    mycol = db[f"{col_name}"]
    count = limits
    cursors = (mycol.find(query).limit(limits))
    for cursor in cursors:
        colls.append(cursor)
    
    return colls,count,page_result

def fun_filters_limit_offset(db,col_name,query,limits,offset,nb_page):
    colls=[]  
    page_result=10
    if limits < page_result: 
        page_result = limits 
        
    else:
        page_result=page_result
    offsets=0
    offsets=offsets+page_result*(nb_page-1)
    mycol = db[f"{col_name}"]
    count = limits
    cursors = (mycol.find(query).skip(offset).limit(limits))
    for cursor in cursors:
        colls.append(cursor)
    return colls,count,page_result

def fun_filters_limit_offset_order(db,col_name,query,limits,offset,field,order,nb_page):
    colls=[]  
    page_result=10
    if limits < page_result: 
        page_result = limits 
        
    else:
        page_result=page_result
    offsets=0
    offsets=offsets+page_result*(nb_page-1)
    mycol = db[f"{col_name}"]
    count = limits
    cursors = mycol.find(query).skip(offset).limit(limits).sort(f"{field}", order)
    for cursor in cursors:
        colls.append(cursor)
    return colls,count,page_result
    

def find_ones(db,col_name,query) :
    colls = []
    mycol = db[f"{col_name}"]
    cursors = mycol.find_one(query)
    colls.append(cursors)
    return colls 


def agregate(db,col_name,agregate_stages):
    colls = []
    mycol = db[f"{col_name}"]
    cursors = mycol.aggregate(agregate_stages)
    for cursor in cursors:
        colls.append(cursor)
    return colls

def update(db,col_name,query,newvalues):
    mycol = db[f"{col_name}"]
    mycol.update_one(query,newvalues)

    return 'success'

def update_mn(db,col_name,query,newvalues):
    mycol = db[f"{col_name}"]
    mycol.update_many(query,newvalues)
    return 'success'

def delete_col(db,col_name):
    mycol = db[f"{col_name}"]
    mycol.drop()
    return 'success'

def insert(db,col_name,query):
    mycol = db[f"{col_name}"]
    mycol.insert_one(query)
    return 'success'

def insert_mn(db,col_name,query):
    mycol = db[f"{col_name}"]
    mycol.insert_many(query)
    return 'success'
    

def rename(db,oldnamen,newname):
    mycol = db[f"{oldnamen}"]
    mycol.rename(f'{newname}', dropTarget = False)
    return 'success'


def delete_one_doc(db,col_name,query):
    mycol = db[f"{col_name}"]
    mycol.delete_one(query)
    return 'success'

def delete_many_doc(db,col_name,query):
    mycol = db[f"{col_name}"]
    mycol.delete_many(query)
    return 'success'

def current_col(dbs):
    col_dict = {}
    index_dict = {}
    count_dict = {}
    client = mongo_create_connect(dbs['host'],int(dbs['port']),maxSevSelDelay)
    dbnames = client.list_database_names()  
    for dbname in dbnames:
        col_dict[f'{dbname}'] = get_all(client,dbname)
    for key ,value in col_dict.items():
        for col_name in value:
            index_dict[f'{key}_{col_name}'] = len(client[f'{key}'][f'{col_name}'].index_information())
            count_dict[f'{key}_{col_name}'] = client[f'{key}'][f'{col_name}'].find().count()
    return col_dict, index_dict,count_dict

def creat_json(mongo_docs):
    docs = pandas.DataFrame(columns=[])
    for num, doc in enumerate(list(mongo_docs)):
        doc["_id"] = str(doc["_id"])
        doc_id = doc["_id"]
        series_obj = pandas.Series( doc, name=doc_id )
        docs = docs.append(series_obj)
    docs.to_json("files/json_file.json")
