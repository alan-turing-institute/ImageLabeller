"""
Forms for the admin view
"""

import os

from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, validators

class DownloadForm(FlaskForm):
    """
    Allow admin users to download the labels as
    a csv or json
    """
    filetype = RadioField(label="output format",
                        choices=[("csv","csv"),("json","json")])
    filename = StringField("Filename", [validators.length(max=300)],
                           default="labels")
