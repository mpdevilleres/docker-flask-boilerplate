# project/__init__.py

#################
#### imports ####
#################

import os

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy
from redis import Redis

################
#### config ####
################
from project.config import THEME_VERSION

app = Flask(__name__,
            static_url_path='/static/' + THEME_VERSION + '/assets')

app.config.from_object(os.environ['APP_SETTINGS'])

####################
#### extensions ####
####################

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)
redis_conn = Redis(host="redis_1", port=6379)

###################
### blueprints ####
###################

from project.apps.user_mgt import user_blueprint

app.register_blueprint(user_blueprint, url_prefix='/usr-mgt')

###################
### flask-login ###
###################

from project.apps.user_mgt.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


########################
#### error handlers ####
########################

@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500

########################
#### filter register ###
########################

from project.utils.jinja_custom import *