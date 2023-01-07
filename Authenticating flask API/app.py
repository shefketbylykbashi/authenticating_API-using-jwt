#Detyra : Zhvillimi i nje API me disa funksione bazike,duke implementuar authentifikimin bazik ose me token

from flask import Flask, request, jsonify, make_response, request, render_template, session, flash,redirect,url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps
import codecs

app = Flask(__name__)


app.config['SECRET_KEY'] = 'b0773f1b9007e927b3584b3d757a79d082da2cef98a3478eba982c2b9b4bf3de'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            
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
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        
        token = jwt.encode({
            'user': request.form['username'],
     
            'exp': expiration_time
            
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})
        
@app.route('/login_token', methods=['GET','POST'])
@token_required
def login_token():
    session['logged_in'] = True

    return render_template('dashboard.html')       

if __name__ == "__main__":
    app.run(debug=True)
