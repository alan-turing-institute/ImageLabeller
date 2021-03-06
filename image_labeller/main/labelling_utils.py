"""
Most of the functions that do the useful work in labelling images
"""

import os
import sys
import random
from flask import current_app

from image_labeller import db
from image_labeller.schema import Category, Label, User, Image


def fill_category_table(categories):
    """
    Categories are those listed in config.py
    """
    for cat in categories:
        c = Category(category_name=cat)
        db.session.add(c)
    db.session.commit()


def get_user(username):
    """
    query the user table for a user_name matching the
    current session_id.
    """
    user_rows = User.query.filter_by(username=username).all()
    if len(user_rows)==0:
        raise RuntimeError("No user found in db")
    return user_rows[-1].user_id


def get_image(user_id):
    """
    Query the image table for an image, then check that the user has not already labelled
    this image.  (If so, pick another one)
    """
    image_is_new = False
    image = None
    while not image_is_new:
        images = Image.query.all()
        if len(images) == 0:
            return None, None, None
        print("Number of images is {}".format(len(images)),file=sys.stderr)
        image_index = random.randint(0,len(images)-1)
        image = images[image_index]
        # check if this user has already seen this image
        label_rows = Label.query.filter_by(user_id=user_id).\
                        filter_by(image_id=image.image_id).all()
        image_is_new = len(label_rows)==0
        if not image_is_new:
            print("Already seen image {} trying another".format(image.image_id),file=sys.stderr)
    if image:
        print("Will display image {} {}".format(image.image_id,image.image_location),file=sys.stderr)
        return image.image_location, image.image_location_is_url, image.image_id
    else:
        return None, None, None



def save_label(user_id, image_id, label, notes):
    """
    Write this label to the database.
    """

    user = User.query.filter_by(user_id=user_id).first()
    image = Image.query.filter_by(image_id=image_id).first()
    category = Category.query.filter_by(category_name=label).first()
    l = Label(category=category, notes=notes,
              user=user, image=image)
    db.session.add(l)
    db.session.commit()
    return True
