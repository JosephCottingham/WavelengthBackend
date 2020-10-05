import os, json
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, send

from Wavelength.config import Config

with open(os.path.join(os.getcwd(), 'AppSettings.Config')) as config_file:
    app_config = json.load(config_file)
    config = Config.get_instance(Config.MODES.get(app_config.get('MODE')))

app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY

# Database SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


from .models.database.sql_models import Message, Room

# db.create_all()
# db.session.commit()


###########################
#### BLUEPRINT CONFIGS ####
#########################
from Wavelength.home_views import homeBlueprint
from Wavelength.api import apiBlueprint

app.register_blueprint(homeBlueprint)
app.register_blueprint(apiBlueprint)


###########################
#### ADMIN CONFIGS #######
#########################

from flask_admin import Admin

admin = Admin(app)

from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Message, db.session))
admin.add_view(ModelView(Room, db.session))

###########################
#### SOCKETIO CONFIGS ####
#########################

socketio = SocketIO(app, cors_allowed_origins="*")
import Wavelength.sockets
