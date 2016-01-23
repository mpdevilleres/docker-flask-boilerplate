# project/apps/user_mgt/form.py

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('Input Correct Username:',
                         validators=[DataRequired()]
                         )
    password = PasswordField('Input Correct Password:',
                             validators=[DataRequired()]
                             )
    remember_me = BooleanField('Remember Me:')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password:',
                             validators=[DataRequired()]
                             )
    new_password = PasswordField('New Password:',
                             validators=[DataRequired()]
                             )
    retry_password =  PasswordField('Re-Enter Password:',
                             validators=[DataRequired()]
                             )
