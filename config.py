from os import environ


WTF_CSRF_ENABLED = True

# Get secret key from environment variable, be sure to set this on the system!
SECRET_KEY = environ['SECRET_KEY']