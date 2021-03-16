from functools import wraps
from flask import request, _request_ctx_stack, abort,session,flash,render_template,g,url_for,redirect
from bson.objectid import ObjectId
#authentification
def required_manager(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if 'user' in  session:
            if g.current_user[1] !='administrator':
                flash('you are not authorized !')  
                return redirect(url_for('client.signup_logins'))
        return f(*args,**kwargs)
    return wrapper 



def required_login(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if 'user' not in  session:
            #flash('please login')
            return redirect(url_for('client.signup_logins'))
        return f(*args,**kwargs)
    return wrapper

def ajax(fn):
   def wrapper(*args, **kwargs):
      def _toDict(obj):
         if isinstance(obj, dict):
            for key in obj.keys():
               obj[key] = _toDict(obj[key])

            return obj

         elif hasattr(obj, "__iter__"):
            return [_toDict(item) for item in obj]

         elif hasattr(obj, "__dict__"):
            return dict([(key, _toDict(value)) for key, value in obj.__dict__.iteritems() if not callable(value) and not key.startswith("_")])

         else:
            if isinstance(obj, ObjectId):
               return str(obj)
            else:
               return obj

      result = fn(*args, **kwargs)
      return _toDict(result)

   return wrapper
