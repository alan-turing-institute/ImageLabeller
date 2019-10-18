"""
WTForms forms for user to enter label
"""
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, validators


class LabelForm(FlaskForm):
    """
    Standard WTForm
    """
#    categories = []
#    def set_categories(cls, categories):
#        categories = categories
  #  categories = ["Gaps","Labrynths","Spots","Other"]
#    cat_radio = RadioField(choices=[(cat,cat) for cat in categories],
 #                          label="Label")
    cat_radio = RadioField(label="Label")

    notes = StringField('Notes:', [validators.optional(),
                                   validators.length(max=300)],
                        default=" ")
