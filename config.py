import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Access%401234@localhost/inventory_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
