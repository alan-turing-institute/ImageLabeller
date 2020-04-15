"""
Useful functions for the user management / authentication side
of the application.
"""
import sys

from flask import current_app
from image_labeller import db
from image_labeller.schema import User


def fill_admin_user_if_empty():
    """
    use the app config to pre-populate the user table with
    an admin user.
    """
    admin_users = User.query.filter_by(is_admin=True).all()
    if len(admin_users)==0:
        user = User(username=current_app.config["ADMIN_USERNAME"],
                    is_admin=True)
        user.set_password(current_app.config["ADMIN_PASSWORD"])
        db.session.add(user)
        db.session.commit()
        print("Added admin user {}".format(user.username), file=sys.stderr)
