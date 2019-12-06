"""
Forms for the admin view
"""

import os

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

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


class UploadForm(FlaskForm):
    """
    Allow admin users to upload either:
    * A JSON file "catalogue" containing a list of dictionaries describing the
    locations of images.
    * A zip file containing a set of images.
    """
#    filefield = FileField(label="choose a file")
    filefield = FileField(label="choose a file",validators=[FileRequired()])
