from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY']='secretKey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models/patient.db' 
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'app.views.auth.login'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.views import auth
from app.views import deskExec
from app.views import pharmacist
from app.views import diagnostic


