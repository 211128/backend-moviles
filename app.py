from flask import Flask,session

from routes.user import users
from routes.restaurant import departments

from decouple import config

import firebase_admin
from firebase_admin import credentials, storage
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


import os





app = Flask(__name__)
cred = credentials.Certificate("utils\depart.json") # Ubicación de tu archivo JSON de credenciales de Firebase
firebase_admin.initialize_app(cred, {'storageBucket': config('STORAGE_BUCKET')}) # Aquí coloca el nombre de tu bucket de Firebase Storage




app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:CtvXdGaewppEuUcjPmpp@containers-us-west-81.railway.app:6456/railway'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['WTF_CSRF_ENABLED'] = False
app.permanent_session_lifetime = timedelta(minutes=2)


app.register_blueprint(users)
app.register_blueprint(departments)










