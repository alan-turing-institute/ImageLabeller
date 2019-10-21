from flask import Blueprint

bp = Blueprint("admin", __name__, url_prefix="/admin")

from image_labeller.admin import routes
