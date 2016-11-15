from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flaskext.markdown import Markdown
from os import environ


app = Flask(__name__, instance_path=environ['FLASK_INSTANCE'])
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

bcrypt = Bcrypt(app)

Markdown(app)


from app import views, models

