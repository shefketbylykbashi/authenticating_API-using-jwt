#Detyra : Zhvillimi i nje API me disa funksione bazike,duke implementuar authentifikimin bazik ose me token

from flask import Flask, request, jsonify, make_response, request, render_template, session, flash,redirect,url_for
import jwt
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

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'logged in currently'
    
@app.route('/public')
def public():
    return 'For Public'

expiration_time = datetime.utcnow() + timedelta(hours=1)

  

@app.route('/login', methods=['GET','POST'])
#qeky funksion thirret saher tbahet qekjo kerkesa
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        

if __name__ == "__main__":
    app.run(debug=True)
