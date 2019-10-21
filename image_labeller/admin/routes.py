import os
from flask import (
    current_app,
    flash,
    redirect,
    request,
    render_template,
    send_file,
    url_for,
    send_from_directory
)

from image_labeller.decorators import admin_required
from image_labeller.admin import bp
from image_labeller.admin.admin_utils import prep_csv, prep_json
from image_labeller.admin.forms import DownloadForm


@bp.route("/download", methods=("GET", "POST"))
#@admin_required
def download():
    """
    Download the contents of the labelling as either a csv or json
    file
    """
    print("GETTING download")
    form = DownloadForm()
    if request.method=="POST":
        print("POSTING download")
        filetype = form.filetype.data
        filename = form.filename.data
        tmpdir = current_app.config["TMPDIR"]
        if filetype == "json":
            return_file = prep_json(filename, tmpdir)
        else:
            return_file = prep_csv(filename, tmpdir)
        print("About to send from directory {} {}".format(tmpdir, return_file))
        try:
            return send_from_directory(tmpdir, return_file, as_attachment=True)
        except FileNotFoundError:
            abort(404)
    return render_template("admin/download.html",form=form)
