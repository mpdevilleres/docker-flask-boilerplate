# project/apps/user_mgt/views.py
from flask import request, render_template, redirect, url_for

# Blueprint Components
from project.apps.user_mgt import user_blueprint
from project.apps.user_mgt.forms import LoginForm

# Utilities
from project import bcrypt

# Extensions
from flask.ext.login import login_user

# Models
from project.apps.user_mgt.models import User


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user is not None and current_user.is_authenticated():
    #     return redirect(url_for('main.index' ))

    if request.method=='POST':
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(username = form.username.data).first()
            if user is None:
                form.username.errors.append('Username not found')
                return render_template('user/login.html',  form = form)

            if not bcrypt.check_password_hash(user.password, form.password.data):
                form.password.errors.append('Password did not match')
                return render_template('user/login.html',  form = form)

            else:
                login_user(user, remember = form.remember_me.data)
                return redirect(url_for('main.index' ))

    return render_template('login.html', form = LoginForm())
