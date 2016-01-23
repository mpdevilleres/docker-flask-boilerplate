# project/apps/user_mgt/models.py

from project import bcrypt
from project import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_groups.id'))

    full_name = db.Column(db.String(60))
    username = db.Column(db.String(60))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    department = db.Column(db.String(60))
    position = db.Column(db.String(60))
    email = db.Column(db.String(60))
    local_number = db.Column(db.String(60))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    section = db.Column(db.Boolean)

    def __init__(self, full_name=None, username=None,
                 first_name=None, last_name=None, department=None,
                 position=None, email=None, local_number=None,
                 password=None, active=None, section=False, group_id=3):

        self.full_name = full_name
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.position = position
        self.email = email
        self.local_number = local_number
        self.active = active
        self.group_id = group_id
        self.password = bcrypt.generate_password_hash(password)
        self.section = section

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<username - {}>'.format(self.username)
