from flask import Flask, render_template, request,url_for,redirect,abort,jsonify,session,flash
import uuid
from utilities import *
from settings import *

#create new client and credential
def signup_login():
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
            return render_template("choice/add_user.html", register=register)

        elif request.form['submit'] == 'Log in':
            user_name= request.form['user_name']
            password=request.form['password']
            try:
                con=postgres_connetion(host,db_name,db_user,db_password)
                cur=con.cursor()
                password_record = get_resource('password','client','user_name',user_name,cur)
                client_id = get_resource('client_id','client','user_name',user_name,cur)

            except Exception as e:
                login = False
                print(e)
                #abort(422)
            finally:
                if(con != None):
                    cur.close()
                    con.close()
            if not password_record:
                login = False
            else:
                checked = check_password(password,password_record[0],pepper)
                if checked :
                    session['permanent'] = False
                    session['user'] = client_id[0]
                    return redirect(url_for("databaseinfo.connect_to_dbs"))
                else:
                    login = False
                    
    return render_template("security/home.html",register = register,login=login)
   
def logout():
    logout = None
    session.pop('user',None)
    logout = True
    return redirect(url_for("client.logouts"))


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






       


            


        




