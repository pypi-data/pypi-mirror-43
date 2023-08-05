import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
connex_app = connexion.App(__name__)
app = connex_app.app

db = SQLAlchemy(app)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Welcome@123@104.199.146.29/mall"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')

db.init_app(app)
ma = Marshmallow(app)
