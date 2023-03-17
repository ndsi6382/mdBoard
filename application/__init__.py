import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tempfile import mkdtemp

DATA_DIR = "/data"
APP = Flask(__name__)
APP.config["SECRET_KEY"] = os.environ["SECRET"]
APP.config["SESSION_FILE_DIR"] = mkdtemp(suffix=".mdb")
APP.config["SESSION_PERMANENT"] = True
APP.config["SESSION_TYPE"] = "filesystem"
if os.environ["SECURE_COOKIE"] == "True":
    APP.config["SESSION_COOKIE_SECURE"] = True
else:
    APP.config["SESSION_COOKIE_SECURE"] = False
APP.config["SESSION_COOKIE_SAMESITE"] = "Strict"
APP.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DATA_DIR, 'database.db')}"
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Session(APP)
DB = SQLAlchemy(APP)

import application.views 
# See https://flask.palletsprojects.com/en/latest/patterns/packages/ for more info.
