#Detyra : Zhvillimi i nje API me disa funksione bazike,duke implementuar authentifikimin bazik ose me token

from flask import Flask, request, jsonify, make_response, request, render_template, session, flash,redirect,url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps
import codecs
import http.cookies

cookie = http.cookies.SimpleCookie()
app = Flask(__name__)


app.config['SECRET_KEY'] = 'b0773f1b9007e927b3584b3d757a79d082da2cef98a3478eba982c2b9b4bf3de'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            token = session['logged_in']
        except:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            global uuu
            uuu = data["user"]
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated

expiration_time = datetime.utcnow() + timedelta(hours=1)
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
         if expiration_time < datetime.utcnow():
            session.clear()
            return render_template('login.html')
         else:
            return render_template('dashboard.html')

    
@app.route('/public')
def public():
    return 'For Public'


@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified!'


@app.route('/login', methods=['GET','POST'])
#qeky funksion thirret saher tbahet qekjo kerkesa
def login():
    if request.form['username'] and request.form['password'] == '12345678910':
 
        
        token = jwt.encode({
            'user': request.form['username'],
     
            'exp': expiration_time
            
        },
            app.config['SECRET_KEY'])
        session['logged_in'] = token
        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})
        

@app.route('/logout', methods=['GET','POST'])
def logout():

    return render_template('login.html')

@app.route('/clear', methods=['GET','POST'])
def clear():
    
    session.clear()
     
    return render_template('login.html')

@app.route('/refresh', methods=['GET','POST'])
@token_required
def refresh():
    print(uuu)
    token = jwt.encode({
            'user': uuu,
            'exp': expiration_time
                
         },
            app.config['SECRET_KEY'])
    session.clear()
    session['logged_in'] = token
    return jsonify({'token': token})

if __name__ == "__main__":
    app.run(debug=True)
