"""
Database schema for SQLAlchemy ORM
"""

from flask import current_app
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from image_labeller import db
from image_labeller import login

class User(UserMixin, db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                        nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(256), nullable=True)
    is_admin = db.Column(db.Boolean(),default=True)
    def __repr__(self):
        return "<User %r>" % self.username

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Image(db.Model):
    __tablename__ = "image"
    image_id = db.Column(db.Integer, primary_key=True,autoincrement=True,
                         nullable=False)
    image_location = db.Column(db.String(100), nullable=False)
    # does image location point to a URL or a local file?
    image_location_is_url = db.Column(db.Boolean, nullable=False)
    image_longitude = db.Column(db.Float, nullable=True)
    image_latitude = db.Column(db.Float, nullable=True)
    image_time = db.column(db.DateTime, nullable=True)


class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                            nullable=False)
    category_name = db.Column(db.String(100), nullable=False)


class Label(db.Model):
    __tablename__ = "label"
    label_id = db.Column(db.Integer, primary_key=True,autoincrement=True,
                         nullable=False)
    category = db.relation("Category", uselist=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    notes = db.Column(db.String(200), nullable=True)
    user = db.relation("User", uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    image = db.relation("Image", uselist=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'))


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
