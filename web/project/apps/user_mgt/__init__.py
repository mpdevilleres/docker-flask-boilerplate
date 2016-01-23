# project/apps/user_mgt/__init__.py

from flask import Blueprint
user_blueprint = Blueprint('user_blueprint', __name__, template_folder='templates')

from project.apps.user_mgt.views import *
