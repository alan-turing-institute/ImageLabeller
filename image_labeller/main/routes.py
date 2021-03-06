"""
Routes for main page of image labelling app
"""
import os
import logging

from flask import render_template, redirect, request, current_app, url_for, session
from flask_login import current_user

from image_labeller import db
from image_labeller.main import bp
from image_labeller.main.forms import LabelForm
from image_labeller.main.labelling_utils import (
    fill_category_table,
    get_user, get_image, save_label
)

logger = logging.getLogger(__name__)

@bp.route("/")
@bp.route("/index")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.not_confirmed"))
    if current_user.is_authenticated:
        user_id = current_user.user_id
        categories = current_app.config["CATEGORIES"]
        fill_category_table(categories)
        title = current_app.config["TITLE"]
        homepage_text = current_app.config["HOMEPAGE_TEXT"]
        return render_template("index.html", title=title,
                               homepage_text=homepage_text)
    return "User not authenticated"


@bp.route("/new",methods=["POST","GET"])
def new_image():
    """
    Display an image, and ask the user to label it
    """
    user_id = current_user.user_id

    categories = current_app.config["CATEGORIES"]
    label_form = LabelForm()
    label_form.cat_radio.choices = [(cat,cat) for cat in categories]
    if request.method=="POST":
        if not "image_id" in session.keys():
            print("No session ID - how did this happen?", file=sys.stderr)
        else:
            image_id = session["image_id"]
            label = label_form.cat_radio.data
            notes = label_form.notes.data
            save_label(user_id, image_id, label, notes)
    # get the next image
    image_location, is_url, image_id = get_image(user_id)

    if not image_location:
        return render_template("no_images.html")
    # store the image id in the session
    session["image_id"] = image_id
    # now reset the form to re-render the page
    new_label_form = LabelForm(formdata=None)
    new_label_form.cat_radio.choices = [(cat,cat) for cat in categories]
    return render_template("new_image.html",
                           new_image=image_location,
                           img_id=image_id,
                           form=new_label_form)
