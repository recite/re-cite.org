# -*- coding: ascii -*-
"""
app
~~~

Main Flask application for the recite project
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils import parse_db_uri

app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.urandom(24)

app.config.from_object('config')

if os.path.isfile(os.path.join(app.root_path, 'instance/config.py')):
    app.config.from_pyfile('config.py')

app.config['SQLALCHEMY_DATABASE_URI'] = parse_db_uri(conf=app.config['DB_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from . import models
from . import views
