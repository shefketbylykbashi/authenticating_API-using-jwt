from flask import Flask, request, jsonify, make_response, request, render_template, session, flash,redirect,url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import make_response
import codecs

app = Flask(__name__)


app.config['SECRET_KEY'] = 'b0773f1b9007e927b3584b3d757a79d082da2cef98a3478eba982c2b9b4bf3de'

expiration_time = datetime.utcnow() + timedelta(hours=1)
    

def protected_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        
        
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
            
                payload = jwt.decode(auth_header, app.config['SECRET_KEY'], algorithms='HS256')
                global uuu
                uuu = payload["user"]
                
            except jwt.exceptions.InvalidTokenError:
                return 'Invalid JWT', 401
        else:
            return 'Authentication required', 401
        return func(*args, **kwargs)
    return decorated

@app.route('/',methods=['GET','POST'])
def home():
    try:
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
    except:
        return render_template('login.html')
    if username and password == '12345678910':
        return render_template('dashboard.html')
    else:
        return render_template('login.html')
        
   
@app.route('/public')
def public():
    return 'For Public'

@app.route('/login', methods=['GET','POST']) 
@protected_token
def login_token():

    return render_template('dashboard.html')

@app.route('/logout', methods=['GET','POST'])
@protected_token
def logout():
    return render_template('login.html')

@app.route('/auth')
@protected_token
def auth():
    return 'JWT is verified!'

@app.route('/get_token', methods=['GET','POST']) 
def login_auth():
    request_body = request.get_json()
    username = request_body['username']
    password = request_body['password']
    if username and password == '12345678910':

        token = jwt.encode({
            'user': username ,
            'exp': expiration_time
                
         },
            app.config['SECRET_KEY'])

        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


@app.route('/refresh', methods=['GET','POST'])
@protected_token
def refresh():
    auth_header = request.headers.get('Authorization')

    token = jwt.encode({
            'user': uuu,
            'exp': expiration_time
                
         },
            app.config['SECRET_KEY'])
    return jsonify({'token': token})

if __name__ == "__main__":
    app.run(debug=True)