from flask import Blueprint

bp = Blueprint('auth', __name__)

from image_labeller.auth import routes
