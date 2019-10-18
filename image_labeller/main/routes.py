"""
Routes for main page of image labelling app
"""
import os
import logging

from flask import render_template, redirect, request, current_app

from image_labeller import db
from image_labeller.main import bp
from image_labeller.main.forms import LabelForm
from image_labeller.main.labelling_utils import (
    fill_user_table, fill_image_table_if_empty,
    fill_category_table,
    get_user, get_image, save_label
)
logger = logging.getLogger(__name__)

@bp.route("/")
@bp.route("/index")
def index():
    fill_user_table()
    fill_image_table_if_empty()
    categories = current_app.config["CATEGORIES"]
    fill_category_table(categories)
    return render_template("index.html", title="Home")


@bp.route("/new",methods=["POST","GET"])
def new_image():
    """
    Display an image, and ask the user to label it
    """
    user_name = "test"
    user_id = get_user(user_name)
    image_filename, image_id = get_image(user_id)
    image_dir = current_app.config["IMAGE_DIR"]
    image_path = os.path.join(image_dir,image_filename)
    categories = current_app.config["CATEGORIES"]
    label_form = LabelForm()
    label_form.cat_radio.choices = [(cat,cat) for cat in categories]
    if request.method=="POST":
        label = label_form.cat_radio.data
        notes = label_form.notes.data
        save_label(user_id, image_id, label, notes)

    # now reset the form to re-render the page
    new_label_form = LabelForm(formdata=None)
    new_label_form.cat_radio.choices = [(cat,cat) for cat in categories]
    return render_template("new_image.html",
                           new_image=image_path,
                           img_id=image_id,
                           form=new_label_form)
