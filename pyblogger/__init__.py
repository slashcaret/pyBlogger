from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '540db43bbec63c5d1ac9fddcb325c00d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
### SQLAlchemy is nothing but a ORM which helps us to use any type of databse
### in object oriented fashion , here we are using sqlite database
### we can switch to any database without chaning the code

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from pyblogger import routes
