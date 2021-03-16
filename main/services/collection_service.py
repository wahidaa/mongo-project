from flask import Flask, render_template, request,url_for,redirect,abort,jsonify,session,g,Response,flash
import json
import pandas as pd
from bson.objectid import ObjectId
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename
import os
from bson.json_util import loads, dumps
import csv
import pandas
from io import StringIO
from utilities import *
from settings import * 


def manage_collection():
    return render_template("result/db_list.html") 

def get_one_collection(database_name,col_name):
    dicts = session['db']
    page= int(request.args.get('page', 1))
    client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
    db=client[database_name]
    [colls,count,page_result] = get_one(db,col_name,page)
    indexes = len(db[f'{col_name}'].index_information())
    current_col = {"database_name":database_name,"col_name":col_name,"count":count,"indexes":indexes }
    session['col'] = current_col
    session['col']['database_name'] = database_name
    session['col']['col_name'] = col_name
    next_page=page+1
    previous=page-1
    results=page_result*page
    if count % page_result == 0:
        max_pages=count//page_result 
    else:
        max_pages=count//page_result +1
    if results>=count and page==1:
        link_next=url_for('collection.get_ones',page=1,key = database_name , i= col_name)
    elif page>1 and results>=count:
        link_next=url_for('collection.get_ones',page=page,key = database_name , i= col_name)
    else:
        link_next=url_for('collection.get_ones',page=next_page,key = database_name , i= col_name)
    if page==1:
        link_previous=url_for('collection.get_ones',page=1,key = database_name , i= col_name)
    else:
        link_previous=url_for('collection.get_ones',page=previous,key = database_name , i= col_name)
    [ids,keys,values] = create_lists(colls)
    return render_template("results/collection_result.html" ,colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)

def get_one_collection_include(database_name,col_name,endpoint):
    dicts = session['db']
    page= int(request.args.get('page', 1))
    client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
    db=client[database_name]
    [colls,count,page_result] = get_one(db,col_name,page)
    indexes = len(db[f'{col_name}'].index_information())
    current_col = {"database_name":database_name,"col_name":col_name,"count":count,"indexes":indexes }
    session['col'] = current_col
    next_page=page+1
    previous=page-1
    results=page_result*page
    if count % page_result == 0:
        max_pages=count//page_result 
    else:
        max_pages=count//page_result +1
    if results>=count and page==1:
        link_next=url_for(f'collection.{endpoint}',page=1,col_name=col_name , database_name = database_name)
    elif page>1 and results>=count:
        link_next=url_for(f'collection.{endpoint}',page=page,col_name=col_name , database_name = database_name)
    else:
        link_next=url_for(f'collection.{endpoint}',page=next_page,col_name= col_name , database_name = database_name)
    if page==1:
        link_previous=url_for(f'collection.{endpoint}',page=1,col_name=col_name , database_name = database_name)
    else:
        link_previous=url_for(f'collection.{endpoint}',page=previous,col_name=col_name , database_name = database_name)
        
    [ids,keys,values] = create_lists(colls)
    return colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages

def get_all_collection(database_name):
    colls =[]
    count_col = {}
    dicts = session['db']
    count = 0
    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        colls = get_all(client,database_name)
        db = client[f'{database_name}']
        for coll in colls:
            col = db[f"{coll}"]
            count = col.count()
            count_col[coll] = count
        session['col']['database_name'] = database_name
    except Exception as e:
        print(e)
    return render_template("results/collections_result.html" ,colls=colls,database_name=database_name,count_col=count_col)

def filter_collection_by_id(database_name,col_name):
    filter_success = None   
    dicts = session['db']
    filter_dict = {}
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filters')
    if request.method=='POST':
        if request.form.get("Send Query"):
            f = request.form
            if (('limit' or 'skip' or 'order') not in f.keys() and f['input_field']) or (('limit' or 'skip' or 'order') in f.keys() and (f['input_field'] and not f['limit'] and not f['skip'] and not f['order'])) :        
                query =request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['field'] and f['order'] and not f['skip'] and not f['limit']):
                print('order')
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['order'] = order
                filter_dict['field'] = field         
                query =request.form['input_field'] 
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif f['limit'] and not f['skip']:
                limits=request.form.get('limit', type=int)
                filter_dict['limits'] = limits           
                query = request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and not f['field'] and not f['order'] ):
                print('skip')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and  f['field'] and f['order'] ):
                print('all')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset
                filter_dict['field'] = field
                filter_dict['order'] = order          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            return redirect(url_for("collection.filter_collection_results_",filter_dict=filter_dict_dps,database_name = database_name,col_name = col_name))
    return render_template("choice/filter_by_id.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages )

def filter_collection_by_id_result(database_name,col_name):
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    filter_dict_dps=request.args.get('filter_dict',{})
    page= int(request.args.get('page', 1))
    filter_success = None
    connection_success = None   
    dicts = session['db']
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filters')
    query = {"_id": ObjectId(f"{filter_dict['query']}")}           
    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        db=client[session['col']['database_name']]
        if ('field' not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            [colls,count,page_result] = fun_filters(db,session['col']['col_name'],query,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order' in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_order(db,session['col']['col_name'],query,field,order,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            limits = filter_dict['limits'] 
            [colls,count,page_result] = fun_filters_limit(db,session['col']['col_name'],query,limits,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            [colls,count,page_result] = fun_filters_limit_offset(db,session['col']['col_name'],query,limits,offset,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order'  in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_limit_offset_order(db,session['col']['col_name'],query,limits,offset,field,order,page)
            filter_success = True
            #connection_success = True
    except Exception as e:
        print(e)
        #connection_success = False
    if filter_success == True:
        return render_template("results/filter_by_id_result.html",colls=colls,filter_success=filter_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],connection_success=connection_success) 
    return render_template("choice/filter_by_id.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps,connection_success=connection_success )
           
def filter_collection(database_name,col_name):
    filter_success = None   
    dicts = session['db']
    filter_dict = {}
    #filter_dict_dps = {}
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filters')
    if request.method=='POST':
        if request.form.get("Send Query"):
            f = request.form
            if (('limit' or 'skip' or 'order') not in f.keys() and f['input_field']) or (('limit' or 'skip' or 'order') in f.keys() and (f['input_field'] and not f['limit'] and not f['skip'] and not f['order'])) :        
                query =request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['field'] and f['order'] and not f['skip'] and not f['limit']):
                print('order')
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['order'] = order
                filter_dict['field'] = field         
                query =request.form['input_field'] 
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif f['limit'] and not f['skip']:
                limits=request.form.get('limit', type=int)
                filter_dict['limits'] = limits           
                query = request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and not f['field'] and not f['order'] ):
                print('skip')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and  f['field'] and f['order'] ):
                print('all')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset
                filter_dict['field'] = field
                filter_dict['order'] = order          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            return redirect(url_for("collection.filter_collection_results",filter_dict=filter_dict_dps,database_name = database_name,col_name = col_name))
    return render_template("choice/filter.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages )

def filter_collection_result(database_name,col_name):
    filter_dict_dps=request.args.get('filter_dict',{})
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    page= int(request.args.get('page', 1))
    filter_success = None
    connection_success = None   
    dicts = session['db']
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filters')            
    try:            
        query = json.loads(filter_dict['query']) 
    except json.decoder.JSONDecodeError as e:
        print(e)
        filter_success = False
    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        db=client[session['col']['database_name']]
        if ('field' not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            [colls,count,page_result] = fun_filters(db,session['col']['col_name'],query,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order' in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_order(db,session['col']['col_name'],query,field,order,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            limits = filter_dict['limits'] 
            [colls,count,page_result] = fun_filters_limit(db,session['col']['col_name'],query,limits,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            [colls,count,page_result] = fun_filters_limit_offset(db,session['col']['col_name'],query,limits,offset,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order'  in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_limit_offset_order(db,session['col']['col_name'],query,limits,offset,field,order,page)
            filter_success = True
    except Exception as e:
        print(e)
    next_page=page+1
    previous=page-1
    results=page_result*page
    if count % page_result == 0:
        max_pages=count//page_result 
    else:
        max_pages=count//page_result +1
    if results>=count and page==1:
        link_next=url_for('collection.filter_collection_results',page=1,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    elif page>1 and results>=count:
        link_next=url_for('collection.filter_collection_results',page=page,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    else:
        link_next=url_for('collection.filter_collection_results',page=next_page,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    if page==1:
        link_previous=url_for('collection.filter_collection_results',page=1,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    else:
        link_previous=url_for('collection.filter_collection_results',page=previous,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    if filter_success == True:
        return render_template("results/filter_result.html",colls=colls,filter_success=filter_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages) 
    return render_template("choice/filter.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps)
           
def filter_comparison(database_name,col_name):
    filter_success = None   
    dicts = session['db']
    filter_dict = {}
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filter_comparisons')
    if request.method=='POST':
        if request.form.get("Send Query"):
            f = request.form
            if (('limit' or 'skip' or 'order') not in f.keys() and f['input_field']) or (('limit' or 'skip' or 'order') in f.keys() and (f['input_field'] and not f['limit'] and not f['skip'] and not f['order'])) :        
                query =request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['field'] and f['order'] and not f['skip'] and not f['limit']):
                print('order')
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['order'] = order
                filter_dict['field'] = field         
                query =request.form['input_field'] 
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif f['limit'] and not f['skip']:
                limits=request.form.get('limit', type=int)
                filter_dict['limits'] = limits           
                query = request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and not f['field'] and not f['order'] ):
                print('skip')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and  f['field'] and f['order'] ):
                print('all')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset
                filter_dict['field'] = field
                filter_dict['order'] = order          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            return redirect(url_for("collection.filter_comparison_collection_results",filter_dict=filter_dict_dps,database_name = database_name,col_name = col_name))
    return render_template("choice/filter_comparison.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages )

def filter_comparison_collection_result(database_name,col_name):
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    filter_dict_dps=request.args.get('filter_dict',{})
    page= int(request.args.get('page', 1))
    filter_success = None
    connection_success = None   
    dicts = session['db']
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filter_comparisons')            
    try:            
        query = json.loads(filter_dict['query']) 
    except json.decoder.JSONDecodeError as e:
        print(e)
        filter_success = False
    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        db=client[session['col']['database_name']]
        if ('field' not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            [colls,count,page_result] = fun_filters(db,session['col']['col_name'],query,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order' in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_order(db,session['col']['col_name'],query,field,order,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            limits = filter_dict['limits'] 
            [colls,count,page_result] = fun_filters_limit(db,session['col']['col_name'],query,limits,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            [colls,count,page_result] = fun_filters_limit_offset(db,session['col']['col_name'],query,limits,offset,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order'  in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_limit_offset_order(db,session['col']['col_name'],query,limits,offset,field,order,page)
            filter_success = True
            connection_success = True
    except Exception as e:
        print(e)
        connection_success = False
    next_page=page+1
    previous=page-1
    results=page_result*page
    if count % page_result == 0:
        max_pages=count//page_result 
    else:
        max_pages=count//page_result +1
    if results>=count and page==1:
        link_next=url_for('collection.filter_comparison_collection_results',page=1,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    elif page>1 and results>=count:
        link_next=url_for('collection.filter_comparison_collection_results',page=page,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    else:
        link_next=url_for('collection.filter_comparison_collection_results',page=next_page,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    if page==1:
        link_previous=url_for('collection.filter_comparison_collection_results',page=1,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    else:
        link_previous=url_for('collection.filter_comparison_collection_results',page=previous,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    if filter_success == True:
        return render_template("results/comparison_result.html",colls=colls,filter_success=filter_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages) 
    return render_template("choice/filter_comparison.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps,connection_success=connection_success )

def filter_logical(database_name,col_name):
    filter_success = None   
    dicts = session['db']
    filter_dict = {}
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filter_logicals')
    if request.method=='POST':
        if request.form.get("Send Query"):
            f = request.form
            if (('limit' or 'skip' or 'order') not in f.keys() and f['input_field']) or (('limit' or 'skip' or 'order') in f.keys() and (f['input_field'] and not f['limit'] and not f['skip'] and not f['order'])) :        
                query =request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['field'] and f['order'] and not f['skip'] and not f['limit']):
                print('order')
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['order'] = order
                filter_dict['field'] = field         
                query =request.form['input_field'] 
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif f['limit'] and not f['skip']:
                limits=request.form.get('limit', type=int)
                filter_dict['limits'] = limits           
                query = request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and not f['field'] and not f['order'] ):
                print('skip')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and  f['field'] and f['order'] ):
                print('all')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset
                filter_dict['field'] = field
                filter_dict['order'] = order          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            return redirect(url_for("collection.filter_logical_collection_results",filter_dict=filter_dict_dps,database_name = database_name,col_name = col_name))
    return render_template("choice/filter_logical.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages )

def filter_logical_collection_result(database_name,col_name):
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    filter_dict_dps=request.args.get('filter_dict',{})
    page= int(request.args.get('page', 1))
    filter_success = None
    connection_success = None   
    dicts = session['db']
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filter_logicals')            
    try:            
        query = json.loads(filter_dict['query']) 
    except json.decoder.JSONDecodeError as e:
        print(e)
        filter_success = False
    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        db=client[session['col']['database_name']]
        if ('field' not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            [colls,count,page_result] = fun_filters(db,session['col']['col_name'],query,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order' in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_order(db,session['col']['col_name'],query,field,order,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            limits = filter_dict['limits'] 
            [colls,count,page_result] = fun_filters_limit(db,session['col']['col_name'],query,limits,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            [colls,count,page_result] = fun_filters_limit_offset(db,session['col']['col_name'],query,limits,offset,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order'  in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_limit_offset_order(db,session['col']['col_name'],query,limits,offset,field,order,page)
            filter_success = True
            connection_success = True
    except Exception as e:
        print(e)
        connection_success = False
    next_page=page+1
    previous=page-1
    results=page_result*page
    if count % page_result == 0:
        max_pages=count//page_result 
    else:
        max_pages=count//page_result +1
    if results>=count and page==1:
        link_next=url_for('collection.filter_logical_collection_results',page=1,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    elif page>1 and results>=count:
        link_next=url_for('collection.filter_logical_collection_results',page=page,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    else:
        link_next=url_for('collection.filter_logical_collection_results',page=next_page,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    if page==1:
        link_previous=url_for('collection.filter_logical_collection_results',page=1,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    else:
        link_previous=url_for('collection.filter_logical_collection_results',page=previous,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    if filter_success == True:
        return render_template("results/logical_result.html",colls=colls,filter_success=filter_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages) 
    return render_template("choice/filter_logical.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps,connection_success=connection_success )

def filter_regular(database_name,col_name):
    filter_success = None   
    dicts = session['db']
    filter_dict = {}
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filter_regulars')
    if request.method=='POST':
        if request.form.get("Send Query"):
            f = request.form
            if (('limit' or 'skip' or 'order') not in f.keys() and f['input_field']) or (('limit' or 'skip' or 'order') in f.keys() and (f['input_field'] and not f['limit'] and not f['skip'] and not f['order'])) :        
                query =request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['field'] and f['order'] and not f['skip'] and not f['limit']):
                print('order')
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['order'] = order
                filter_dict['field'] = field         
                query =request.form['input_field'] 
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif f['limit'] and not f['skip']:
                limits=request.form.get('limit', type=int)
                filter_dict['limits'] = limits           
                query = request.form['input_field']
                filter_dict['query'] = query
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and not f['field'] and not f['order'] ):
                print('skip')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            elif (f['limit'] and f['skip'] and  f['field'] and f['order'] ):
                print('all')
                limits=request.form.get('limit', type=int)
                offset=request.form.get('skip', type=int)
                field = request.form['field']
                order=request.form.get('order', type=int)
                filter_dict['limits'] = limits
                filter_dict['offset'] = offset
                filter_dict['field'] = field
                filter_dict['order'] = order          
                query =request.form['input_field']
                filter_dict['query'] = query 
                filter_dict_dps=(json.dumps(filter_dict))
            return redirect(url_for("collection.filter_regular_collection_results",filter_dict=filter_dict_dps,database_name = database_name,col_name = col_name))
    return render_template("choice/filter_regular.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages )   

def filter_regular_collection_result(database_name,col_name):
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    filter_dict_dps=request.args.get('filter_dict',{})
    page= int(request.args.get('page', 1))
    filter_success = None
    connection_success = None   
    dicts = session['db']
    ids = []
    keys = []
    values = []
    colls = []
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'filter_regulars')            
    try:            
        query = json.loads(filter_dict['query']) 
    except json.decoder.JSONDecodeError as e:
        print(e)
        filter_success = False
    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        db=client[session['col']['database_name']]
        if ('field' not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            [colls,count,page_result] = fun_filters(db,session['col']['col_name'],query,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order' in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' not in filter_dict.keys()) :
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_order(db,session['col']['col_name'],query,field,order,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' not in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            limits = filter_dict['limits'] 
            [colls,count,page_result] = fun_filters_limit(db,session['col']['col_name'],query,limits,page)
            filter_success = True
        elif ('field'not in filter_dict.keys() and 'order' not in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            [colls,count,page_result] = fun_filters_limit_offset(db,session['col']['col_name'],query,limits,offset,page)
            filter_success = True
        elif ('field' in filter_dict.keys() and 'order'  in filter_dict.keys() and 'offset' in filter_dict.keys() and 'limits' in filter_dict.keys()) : 
            offset = filter_dict['offset']
            limits = filter_dict['limits']
            field = filter_dict['field'] 
            order = filter_dict['order']
            [colls,count,page_result] = fun_filters_limit_offset_order(db,session['col']['col_name'],query,limits,offset,field,order,page)
            filter_success = True
            connection_success = True
    except Exception as e:
        print(e)
        connection_success = False
    next_page=page+1
    previous=page-1
    results=page_result*page
    if count % page_result == 0:
        max_pages=count//page_result 
    else:
        max_pages=count//page_result +1
    if results>=count and page==1:
        link_next=url_for('collection.filter_regular_collection_results',page=1,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    elif page>1 and results>=count:
        link_next=url_for('collection.filter_regular_collection_results',page=page,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    else:
        link_next=url_for('collection.filter_regular_collection_results',page=next_page,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    if page==1:
        link_previous=url_for('collection.filter_regular_collection_results',page=1,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    else:
        link_previous=url_for('collection.filter_regular_collection_results',page=previous,database_name = database_name , col_name= col_name,filter_dict=filter_dict_dps)
    if filter_success == True:
        return render_template("results/regular_result.html",colls=colls,filter_success=filter_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages) 
    return render_template("choice/filter_regular.html",filter_success=filter_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps,connection_success=connection_success )

def agregate_collection(database_name,col_name):
    agregate_success = None
    colls = []
    filter_dict = {}
    dicts = session['db']
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'agregates')
    if request.method=='POST':
        if request.form.get("Send Query"):
            agregate_stages = request.form['agregate']
            filter_dict['agregate_stages'] = agregate_stages
            filter_dict_dps=(json.dumps(filter_dict))            
            return redirect(url_for("collection.agregate_collection_results",filter_dict=filter_dict_dps,database_name = database_name,col_name = col_name))
    return render_template("choice/agregate.html",database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages )

def agregate_collection_result(database_name,col_name):
    filter_dict_dps=request.args.get('filter_dict',{})
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    page= int(request.args.get('page', 1))
    agregate_success = None
    colls = []
    skip = 0
    limit = 5
    dicts = session['db']         
    try:            
        agregate_stages = json.loads(filter_dict['agregate_stages']) 
        print(agregate_stages)
        agregate_list = [] 
        for agregate_stage in agregate_stages:
            agregate_list.extend(list(agregate_stage.keys()))
        stages = ','.join(agregate_list)
    except json.decoder.JSONDecodeError as e:
        print(e)
        agregate_success = False

    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        db=client[session['col']['database_name']]
        colls = agregate(db,session['col']['col_name'],agregate_stages)
        agregate_success = True
    except Exception as e:
        print(e)
        agregate_success = False
    return render_template("results/agregate_result.html",colls=colls,agregate_success=agregate_success, stages=stages, filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name']) 
    return render_template("choice/agregate.html",agregate_success=agregate_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,filter_dict=filter_dict_dps )

def delete_collection(database_name,col_name):
    delete_success = None
    count_col = 0
    count_db = 0
    dicts = session['db']
    if request.method=='POST':
        if request.form['submit'] == 'Delete':
            try:
                client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
                db=client[database_name]
                delete_col(db,col_name)
                dbnames = client.list_database_names()
                count_db = len(dbnames)
                session['count_db'] = count_db
                for dbname in dbnames:
                    if dbname not in ['admin','config']:
                        count_col += len(client[f'{dbname}'].collection_names())
                session['count_col'] = count_col
                delete_success = True
            except Exception as e:
                print(e)
                delete_success = False
            return redirect(url_for("collection.get_all_collections",database_name=database_name,delete_success=delete_success))

def create_new_collection(key):
    count_col = 0
    count_db = 0
    dicts = session['db']
    session['col']['database_name'] = key
    if request.method=='POST':
        if request.form['submit'] == 'Send':
            col_name = request.form['col_name']
            try:
                client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
                db=client[f"{key}"]
                insert(db,col_name,{})
                mycol = db[f"{col_name}"]
                x = mycol.delete_many({})
                dbnames = client.list_database_names()
                count_db = len(dbnames)
                session['count_db'] = count_db
                for dbname in dbnames:
                    if dbname not in ['admin','config']:
                        count_col += len(client[f'{dbname}'].collection_names())
                session['count_col'] = count_col        
            except Exception as e:
                print(e)
        return redirect(url_for("collection.get_all_collections",database_name=key))
    return render_template("choice/create_col.html",key=key)

def update_collection(database_name,col_name,id):
    update_success = None
    dicts = session['db']
    if request.method=='POST':
        if request.form['submit'] == 'Send Query':
            try:
                new_values = json.loads(request.form['new_values'])
            except json.decoder.JSONDecodeError as e:
                print(e)
                update_success = False
            query = {"_id": ObjectId(f"{id}")}
            try:
                client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
                db=client[session['col']['database_name'] ]
                [colls,count,page_result] = fun_filters(db,session['col']['col_name'] ,query,1)
                update(db,session['col']['col_name'] ,query,new_values)
                update_success = True
            except Exception as e:
                print(e)
                update_success = False
            if update_success == True:
                return redirect(url_for("collection.get_ones",update_success=update_success,key = session['col']['database_name'], i = session['col']['col_name'] ,id = id))
    return render_template("choice/update.html",update_success=update_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],id=id )

def update_many_collection(database_name,col_name):
    update_success = None
    dicts = session['db']
    filter_dict = {}
    filter_dict_dps = {}
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'update_many_collections')
    if request.method=='POST':
        if request.form['submit'] == 'Send Query':
            query = request.form['query']
            new_values = request.form['new_values']
            filter_dict['query'] = query
            filter_dict['new_values'] = new_values
            filter_dict_dps=(json.dumps(filter_dict))
        return redirect(url_for("collection.update_mn_collection_results",filter_dict=filter_dict_dps,database_name = database_name,col_name = col_name )) 
    return render_template("choice/update_many.html",update_success=update_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps)  

def update_mn_collection_result(database_name,col_name):
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    filter_dict_dps=request.args.get('filter_dict',{})
    connection_success = None   
    update_success = None
    colls = []
    colls_result = []
    ids = []
    dicts = session['db']
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'update_many_collections')            
    try:            
        query = json.loads(filter_dict['query'])
        new_values = json.loads(filter_dict['new_values']) 
    except json.decoder.JSONDecodeError as e:
        print(e)
        update_success = False

    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        db=client[session['col']['database_name'] ]
        [colls,count,page_result] = fun_filters(db,session['col']['col_name'] ,query,1)
        if not colls:
            update_success = False
        else:
            [colls_result,count,page_result] = fun_filters(db,session['col']['col_name'] ,query,1)
            update_mn(db,session['col']['col_name'],query,new_values)
            update_success = True
            for i in range(len(colls_result)):
                ids.append(fun_filters(db,session['col']['col_name'] ,{"_id": ObjectId(f"{colls_result[i]['_id']}")},1)[0][0])
            colls_result = ids
    except Exception as e:
        print(e)
        update_success = False    
    return render_template("results/update_result.html",colls_result=colls_result,update_success=update_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],connection_success=connection_success) 
    return render_template("choice/update_many.html",update_success=update_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps,connection_success=connection_success )

def insert_collection(database_name,col_name):
    insert_success = None
    dicts = session['db']
    filter_dict = {}
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'inserts')
    if request.method=='POST':
        if request.form['submit'] == 'Send Query':
            query = request.form['query']
            filter_dict['query'] = query
            filter_dict_dps=(json.dumps(filter_dict))
            return redirect(url_for("collection.insert_collection_results",filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name']))
    return render_template("choice/insert.html",insert_success=insert_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)

def insert_collection_result(database_name,col_name):
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    filter_dict_dps=request.args.get('filter_dict',{})
    connection_success = None   
    insert_success = None
    count = 1
    colls = []
    colls_result = []
    dicts = session['db']
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'inserts')            
    try:            
        query = json.loads(filter_dict['query'])
    except json.decoder.JSONDecodeError as e:
        print(e)
        insert_success = False

    try:
        client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
        db=client[session['col']['database_name'] ]
        insert(db,session['col']['col_name'] ,query)
        colls_result.append(query)
        col_dict, index_dict,count_dict = current_col(session['db'])
        session['col']['count'] = count_dict[f"{session['col']['database_name']}_{session['col']['col_name']}"]
        insert_success = True
    except Exception as e:
        print(e)
        insert_success = False
    if insert_success == True:
        return render_template("results/insert_result.html",colls_result=colls_result,insert_success=insert_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],connection_success=connection_success,count=count) 
    return render_template("choice/insert.html",insert_success=insert_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps,connection_success=connection_success )

def insert_mn_collection(database_name,col_name):
    insert_success = None
    dicts = session['db']
    filter_dict = {}
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'inserts_collection') 
    if request.method=='POST':
        if request.form['submit'] == 'Send Query':
            query = request.form['query']
            filter_dict['query'] = query
            filter_dict_dps=(json.dumps(filter_dict))
            return redirect(url_for("collection.insert_mn_collection_results",filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name']))
    return render_template("choice/insert_many.html",insert_success=insert_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages )

def insert_mn_collection_result(database_name,col_name):
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    filter_dict_dps=request.args.get('filter_dict',{})
    connection_success = None   
    insert_success = None
    colls = []
    colls_result = []
    dicts = session['db']
    count = 0
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'inserts_collection')
    if filter_dict:            
        try:            
            query = json.loads(filter_dict['query'])
        except json.decoder.JSONDecodeError as e:
            print(e)
            insert_success = False

        try:
            client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
            db=client[session['col']['database_name'] ]
            count = len(query)
            insert_mn(db,session['col']['col_name'],query)
            col_dict, index_dict,count_dict = current_col(session['db'])
            session['col']['count'] = count_dict[f"{session['col']['database_name']}_{session['col']['col_name']}"]
            insert_success = True
        except Exception as e:
            print(e)
            insert_success = False
        
        return render_template("results/insert_mn_result.html",colls_result=query,insert_success=insert_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],connection_success=connection_success,count=count) 
    return render_template("choice/insert_many.html",insert_success=insert_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps,connection_success=connection_success )
 
def insert_file(database_name,col_name):
    dicts = session['db']
    insert_file_success = None
    count = 0
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if 'csv' == file.filename.split('.')[1]:
                try:
                    data = pd.read_csv(file,encoding = 'ISO-8859-1')
                    payload = json.loads(data.to_json(orient='records'))
                except:
                    insert_file_success = False
            elif 'json' == file.filename.split('.')[1]:
                myfile = file.read()
                try:
                    payload = json.loads(myfile)
                except json.decoder.JSONDecodeError as e:
                    insert_file_success = False
                    print(e)
                    
        try:
            client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
            count = len(payload)
            db=client[session['col']['database_name'] ]
            insert_mn(db,session['col']['col_name'],payload)
            col_dict, index_dict,count_dict = current_col(session['db'])
            session['col']['count'] = count_dict[f"{session['col']['database_name']}_{session['col']['col_name']}"]
            insert_file_success = True
        except Exception as e:
            insert_file_success = False
            print(e)
    return render_template('choice/insert_csv_file.html',database_name = session['col']['database_name'], col_name = session['col']['col_name'],insert_file_success=insert_file_success,count=count)

def export_file(key,i):
    export_success = None
    if request.method == "POST":
        if 'export_csv' in request.form.keys():
            if request.form['input_field']:
                try:
                    query = json.loads(request.form['input_field'])
                except:
                    flash("No Result , Try to modify your query")
                    export_success = False
                    return redirect(url_for("collection.get_ones",export_success=export_success,key=key,i=i))
            else: 
                query = {}
            dicts = session['db']
            try:
                client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
                db=client[session['col']['database_name']]
                coll = db[session['col']['col_name']]
                mongo_docs = coll.find(query)
                # if len(list(mongo_docs)) == 0:
                #     flash("there is no matched documents")
                #     return redirect(url_for("collection.get_ones",export_success=export_success,key=key,i=i))
                fieldnames = list(mongo_docs[0].keys())
                docs = pandas.DataFrame(mongo_docs)
                file_buffer = StringIO()
                docs.to_csv(file_buffer, ",", index=False)
                file_buffer.seek(0)
                return Response(
                file_buffer,
                mimetype="text/csv",
                headers={"Content-disposition":
                            "attachment; filename=csv_file.csv"})
            except Exception as e:
                print(e)
                export_success = False
                flash("fail to export")
                return redirect(url_for("collection.get_ones",export_success=export_success,key=key,i=i))

        elif 'export_json' in request.form.keys():
            if request.form['input_field']:
                try:
                    query = json.loads(request.form['input_field'])
                except Exception as e:
                    print(e)
                    flash("No Result , Try to modify your query")
                    export_success = False
                    return redirect(url_for("collection.get_ones",export_success=export_success,key=key,i=i))
            else: 
                query = {}
            dicts = session['db']
            try:
                client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
                db=client[session['col']['database_name']]
                coll = db[session['col']['col_name']]
                mongo_doc = coll.find(query)
                if len(list(mongo_doc)) == 0:
                    flash("there is no matched documents")
                    return redirect(url_for("collection.get_ones",export_success=export_success,key=key,i=i))
                mongo_docs = list(mongo_doc)
                docs = pandas.DataFrame(columns=[])
                for num, doc in enumerate(list(mongo_docs)):
                    doc["_id"] = str(doc["_id"])
                    doc_id = doc["_id"]
                    series_obj = pandas.Series( doc, name=doc_id )
                    docs = docs.append(series_obj)
                file_buffer = StringIO()
                docs.to_json(file_buffer)
                file_buffer.seek(0)
                return Response(
                file_buffer,
                mimetype="text/csv",
                headers={"Content-disposition":
                            "attachment; filename=json_file.json"})
            except Exception as e:
                print(e)
                export_success = False
                flash("fail to export")
                return redirect(url_for("collection.get_ones",export_success=export_success,key=key,i=i))
    return redirect(url_for("collection.get_ones",export_success=export_success,key=key,i=i))

def delete_one_document(database_name,col_name,id):
    delete_success = None
    dicts = session['db']
    if request.method=='POST':
        if request.form['submit'] == 'Delete':
            try:
                client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
                db=client[session['col']['database_name'] ]
                query = {"_id": ObjectId(f"{id}")}
                [colls,count,page_result] = fun_filters(db,session['col']['col_name'] ,query,1)
                delete_one_doc(db,session['col']['col_name'],query)
                col_dict, index_dict,count_dict = current_col(session['db'])
                session['col']['count'] = count_dict[f"{session['col']['database_name']}_{session['col']['col_name']}"]
                delete_success = True
            except Exception as e:
                print(e) 
                delete_success = False
            return redirect(url_for("collection.get_ones",delete_success=delete_success,key = session['col']['database_name'], i = session['col']['col_name'] ,id = id))

def delete_many_document(database_name,col_name):
    delete_success = None
    dicts = session['db']
    filter_dict = {}
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'delete_many_documents')
    if request.method=='POST':
        if request.form['submit'] == 'Send Query':
            query = request.form['query']
            filter_dict['query'] = query
            filter_dict_dps=(json.dumps(filter_dict))
            
            return redirect(url_for("collection.delete_mn_document_results",filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name']))
    return render_template("choice/delete_many_documents.html",delete_success=delete_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)

def delete_mn_document_result(database_name,col_name):
    filter_dict=json.loads(request.args.get('filter_dict',{}))
    filter_dict_dps=request.args.get('filter_dict',{})
    connection_success = None   
    delete_success = None
    colls = []
    colls_result = []
    dicts = session['db']
    [colls ,database_name ,col_name,link_next,link_previous,page,page_result,max_pages] =get_one_collection_include(database_name,col_name,'delete_many_documents')
    if filter_dict:            
        try:            
            query = json.loads(filter_dict['query'])
        except json.decoder.JSONDecodeError as e:
            print(e)
            insert_success = False
        try:
            client = mongo_create_connect(dicts['host'],dicts['port'],maxSevSelDelay)
            db=client[session['col']['database_name'] ]
            [colls,count,page_result] = fun_filters(db,session['col']['col_name'] ,query,1)
            if not colls:
                delete_success = False
            else:
                delete_many_doc(db,session['col']['col_name'],query)
                col_dict, index_dict,count_dict = current_col(session['db'])
                session['col']['count'] = count_dict[f"{session['col']['database_name']}_{session['col']['col_name']}"]
                delete_success = True
        except Exception as e: 
            print(e)
            delete_success = False
            
        return render_template("results/delete_mn_result.html",colls=colls,delete_success=delete_success,filter_dict=filter_dict_dps,database_name = session['col']['database_name'], col_name = session['col']['col_name'],connection_success=connection_success) 
    return render_template("choice/delete_many_documents.html",delete_success=delete_success,database_name = session['col']['database_name'], col_name = session['col']['col_name'],colls= colls ,key = database_name , i= col_name,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,filter_dict=filter_dict_dps,connection_success=connection_success )

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