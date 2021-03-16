from flask import Flask, render_template, request,url_for,redirect,abort,jsonify,session,g
import json
from flask_paginate import Pagination, get_page_args
from utilities import *
from settings import * 

def get_all_clients():
    page= int(request.args.get('page', 1))
    first_name = []
    last_name = []
    email = []
    try:
        con=postgres_connetion(host,db_name,db_user,db_password)
        cur=con.cursor()
        #records = get_all_resources('client',cur)
        [count,page_result,records] = get_list_clients(cur,page)
        next_page=page+1
        previous=page-1
        results=page_result*page
        if count % page_result == 0:
            max_pages=count//page_result - 1
        else:
            max_pages=count//page_result  
        if results>=count and page==1:
            link_next=url_for('administrator.get_all_clientss',page=1)
        elif page>1 and results>=count:
            link_next=url_for('administrator.get_all_clientss',page=page)
        else:
            link_next=url_for('administrator.get_all_clientss',page=next_page)
        if page==1:
            link_previous=url_for('administrator.get_all_clientss',page=1)
        else:
            link_previous=url_for('administrator.get_all_clientss',page=previous)
        for record in records:
            first_name.append(record[1])
            last_name.append(record[2])
            email.append(record[4])

    except Exception as e:
        login = False
        print(e)
        #abort(422)
    finally:
        if(con != None):
            cur.close()
            con.close()
    return render_template("results/client_list.html",email=email,first_name=first_name,last_name=last_name,
    link_next=link_next,link_previous=link_previous,page=page,count=count,max_pages=max_pages)


def get_all_users():
    page= int(request.args.get('page', 1))
    first_name = []
    last_name = []
    email = []
    try:
        con=postgres_connetion(host,db_name,db_user,db_password)
        cur=con.cursor()
        
        [count,page_result,records] = get_list_clients_by_type(cur,page,'user')
        next_page=page+1
        previous=page-1
        results=page_result*page
        if count % page_result == 0:
            max_pages=count//page_result - 1
        else:
            max_pages=count//page_result  
        if results>=count and page==1:
            link_next=url_for('administrator.get_all_clientss',page=1)
        elif page>1 and results>=count:
            link_next=url_for('administrator.get_all_clientss',page=page)
        else:
            link_next=url_for('administrator.get_all_clientss',page=next_page)
        if page==1:
            link_previous=url_for('administrator.get_all_clientss',page=1)
        else:
            link_previous=url_for('administrator.get_all_clientss',page=previous)
        for record in records:
            first_name.append(record[1])
            last_name.append(record[2])
            email.append(record[4])

    except Exception as e:
        login = False
        print(e)
        #abort(422)
    finally:
        if(con != None):
            cur.close()
            con.close()
    return render_template("results/client_list.html",email=email,first_name=first_name,last_name=last_name,
    link_next=link_next,link_previous=link_previous,page=page,count=count,max_pages=max_pages)

def get_all_administrators():
    page= int(request.args.get('page', 1))
    first_name = []
    last_name = []
    email = []
    try:
        con=postgres_connetion(host,db_name,db_user,db_password)
        cur=con.cursor()
        
        [count,page_result,records] = get_list_clients_by_type(cur,page,'administrator')
        next_page=page+1
        previous=page-1
        results=page_result*page
        if count % page_result == 0:
            max_pages=count//page_result - 1
        else:
            max_pages=count//page_result  
        if results>=count and page==1:
            link_next=url_for('administrator.get_all_clientss',page=1)
        elif page>1 and results>=count:
            link_next=url_for('administrator.get_all_clientss',page=page)
        else:
            link_next=url_for('administrator.get_all_clientss',page=next_page)
        if page==1:
            link_previous=url_for('administrator.get_all_clientss',page=1)
        else:
            link_previous=url_for('administrator.get_all_clientss',page=previous)
        for record in records:
            first_name.append(record[1])
            last_name.append(record[2])
            email.append(record[4])

    except Exception as e:
        login = False
        print(e)
        #abort(422)
    finally:
        if(con != None):
            cur.close()
            con.close()
    return render_template("results/client_list.html",email=email,first_name=first_name,last_name=last_name,
    link_next=link_next,link_previous=link_previous,page=page,count=count,max_pages=max_pages)



def add_user():
    output_client={}
    output_cridential={}
    port_list = []
    host_list = []
    connection_record = {}
    register = None
    login = None
    if request.method=='POST':
        if request.form['submit'] == 'Sign Up':
            f = request.form
            client_id=str(uuid.uuid4())
            cridential_id=str(uuid.uuid4())     
            first_name= request.form['first_name']
            last_name=request.form['last_name']
            email=request.form['email']
            if 'user type' in request.form.keys():
                print('hello')
                user_type=request.form['user type']
            else:
                user_type = 'user'
            user_name=request.form['user_name']
            password=request.form['password']
            output_client ={
                'client_id':client_id,
                'first_name':first_name,
                'last_name':last_name,
                'user_type':user_type,
                'email':email,
                'user_name':user_name,
                'password':hash_string(password,pepper)
            }
            try:
                con=postgres_connetion(host,db_name,db_user,db_password)
                cur=con.cursor()
                post_resource(output_client,'client',cur)
                con.commit()
                register = True
            except Exception as e:
                register = False
                print(e)
                #abort(422)
            finally:
                if(con != None):
                    cur.close()
                    con.close()
    return render_template("choice/add_user.html",register=register)