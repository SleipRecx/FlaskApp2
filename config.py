import os

# default configuration for the application
class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = os.urandom(24)
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SESSION_COOKIE_NAME = "User Information"

# configuration for development
class DevelopmentConfig(BaseConfig):
	DEBUG = True	

# configuration for production
class ProductionConfig(BaseConfig):
	DEBUG = False	