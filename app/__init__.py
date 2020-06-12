import importlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
import sys
importlib.reload(sys)
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
from flask_mail import Mail
mail = Mail()
mail.init_app(app)