"""
WTForms forms for user to enter label
"""
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, validators


class LabelForm(FlaskForm):
    """
    Assign a category, and optionally notes, to an image.
    The choices for the RadioField will be set in routes.py, according
    to the current_app's config.
    """
    cat_radio = RadioField(label="Label")

    notes = StringField('Notes:', [validators.optional(),
                                   validators.length(max=300)],
                        default=" ")
