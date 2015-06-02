import os

# default configuration for the application
class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = '^Ta\xa7\x1e\xc8\xe3#a\xb6\xe5<H\xf0\xd2\xb3\xbb\x1a\x90(p\x8f\x95\xdb'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SESSION_COOKIE_NAME = "User Information"

# configuration for development
class DevelopmentConfig(BaseConfig):
	DEBUG = True	

# configuration for production
class ProductionConfig(BaseConfig):
	DEBUG = False	=""