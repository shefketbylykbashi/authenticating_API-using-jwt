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

if __name__ == "__main__":
    app.run(debug=True)