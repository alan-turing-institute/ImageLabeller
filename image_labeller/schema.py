"""
Database schema for SQLAlchemy ORM
"""

from flask import current_app
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from image_labeller import db
from image_labeller import login

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                        nullable=False)
    user_name = db.Column(db.String(100), nullable=False)


class Image(db.Model):
    __tablename__ = "image"
    image_id = db.Column(db.Integer, primary_key=True,autoincrement=True,
                         nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)


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
