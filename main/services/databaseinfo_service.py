from flask import Flask, render_template, request,url_for,redirect,abort,jsonify,session,g,flash
import json
import uuid
from pymongo import MongoClient
from utilities import *
from settings import *

#connect to mongodb
def connect_to_db():
    connection = {}
    col_dict = {}
    db_list = {}
    count_col = 0
    count_db = 0
    connection_success = None
    if request.method=='POST':
        if request.form['submit'] == 'Connect':
            database_port=request.form.get('database_port', type=int)
            database_host=request.form['database_host']
            user_name=request.form['user_name']
            password=request.form['password']
            db_dict = {
                'port':database_port,
                'host':database_host
            }
            connection = {
                'database_user_name':user_name,
                'database_host':database_host,
                'database_port':database_port,
                'database_password':password,
                'client_id':session['user']
            }
            try:
                client = mongo_create_connect(database_host,database_port,maxSevSelDelay)
                dbnames = client.list_database_names()
                count_db = len(client.list_database_names())
                session['count_db'] = count_db
                for dbname in dbnames:
                    if dbname not in ['admin','config']:
                        count_col += len(client[f'{dbname}'].collection_names())
                    col_dict[dbname] = get_all(client,dbname)
                session['count_col'] = count_col
                db_dict['col'] = col_dict        
                session['db'] = db_dict
                connection_success = True
            except Exception as e:
                print(e)
                connection_success = False
            if connection_success == True:
                try:
                    
                    con=postgres_connetion(host,db_name,db_user,db_password)
                    cur=con.cursor()
                    records = get_resources_by_filter('databaseinfo','client_id',session['user'],cur)
                    if records:
                        for record in records:
                            if record[2] != connection['database_host'] or record[3] != connection['database_port']:  
                                post_resource_1(connection,'databaseinfo',cur)
                                con.commit()
                    else:
                        post_resource_1(connection,'databaseinfo',cur)
                        con.commit()
                                      
                except Exception as e:
                    print(e)
                    #abort(422)
                finally:
                    if(con != None):
                        cur.close()
                        con.close()
                return redirect(url_for("databaseinfo.db_lists")) 
    return render_template("security/connect_to_db.html", connection_success=connection_success)

def db_list():
    return render_template("security/db_list.html")

def delete_database(key):
    delete_db_success = None
    count_col = 0
    count_db = 0
    dicts = session['db']
    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        client.drop_database(f'{key}')
        dbnames = client.list_database_names()
        count_db = len(dbnames)
        session['count_db'] = count_db
        for dbname in dbnames:
            if dbname not in ['admin','config']:
                count_col += len(client[f'{dbname}'].collection_names())
        session['count_col'] = count_col
        delete_db_success = True
    except Exception as e:
        delete_db_success = False
        print(e)
    return redirect(url_for("databaseinfo.db_lists"))

def create_new_database():
    dicts = session['db']
    creation_success = None
    count_col = 0
    count_db = 0
    if request.method=='POST':
        if request.form['submit'] == 'Send':
            database_name = request.form['database_name']
            col_name = request.form['col_name']
            try:
                client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
                db=client[f"{database_name}"]
                insert(db,f"{col_name}",{})
                mycol = db[f"{col_name}"]
                x = mycol.delete_many({})
                dbnames = client.list_database_names()
                count_db = len(dbnames)
                session['count_db'] = count_db 
                for dbname in dbnames:
                    if dbname not in ['admin','config']:
                        count_col += len(client[f'{dbname}'].collection_names())
                session['count_col'] = count_col
                creation_success = True       
            except Exception as e:
                print(e)
            return redirect(url_for("databaseinfo.db_lists"))


def recent_connection(database_host,database_port):
    col_dict = {}
    count_col = 0
    record = None
    db_dict = {
        'port':int(database_port),
        'host':database_host
    }
    try:
        client = mongo_create_connect(database_host,int(database_port),maxSevSelDelay)
        dbnames = client.list_database_names()
        count_db = len(dbnames)
        session['count_db'] = count_db
        for dbname in dbnames:
            col_dict[dbname] = get_all(client,dbname)
            count_col += len(client[f'{dbname}'].collection_names())
        session['count_col'] = count_col
        db_dict['col'] = col_dict        
        session['db'] = db_dict
        connection_success = True
    except Exception as e:
        print(e)
        connection_success = False  
    return redirect(url_for("databaseinfo.db_lists"))
#database logout
def db_logout():
    logoutdb = None
    session.pop('db',None)
    session.pop('db2',None)
    logoutdb = True
    return render_template("security/connect_to_db.html",logoutdb = logoutdb)


  
# errors      
def error_422(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
def error_400(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400
def error_404(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404