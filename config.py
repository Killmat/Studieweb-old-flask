from os import environ
from os.path import join
from app import app


WTF_CSRF_ENABLED = True

# Get secret key from environment variable, be sure to set this on the system!
SECRET_KEY = environ['SECRET_KEY']

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(app.instance_path, 'app.db')
SQLALCHEMY_MIGRATE_REPO = join(app.instance_path, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False;