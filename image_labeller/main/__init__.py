"""
Main page for image labelling app
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from image_labeller.main import routes
