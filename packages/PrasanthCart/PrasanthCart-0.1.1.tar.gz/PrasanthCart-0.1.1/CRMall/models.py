from config import *
from datetime import datetime
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
import os
import datetime
from sqlalchemy.orm import relationship

app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://prasanth:tiger@localhost/mall"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

#Roles table
class Roles(db.Model):
    __tablename__ = "roles"
    id         = db.Column(db.Integer, primary_key = True)
    name       = db.Column(db.String(50))
    status     = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())

db.create_all()
db.session.commit()
if __name__ == '__main__':
    manager.run()
