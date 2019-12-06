import os
import sys

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
from werkzeug.utils import secure_filename

from image_labeller.decorators import admin_required
from image_labeller.admin import bp
from image_labeller.admin.admin_utils import (
    prep_csv,
    prep_json,
    upload_image,
    upload_images_from_catalogue,
    allowed_file
)
from image_labeller.admin.forms import DownloadForm, UploadForm


@bp.route("/download", methods=["GET", "POST"])
@admin_required
def download():
    """
    Download the contents of the labelling as either a csv or json
    file
    """
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


@bp.route("/upload", methods=["GET","POST"])
@admin_required
def upload():
    """
    upload a catalogue containing
    """
    fileform = UploadForm()
    if request.method == "POST":
        print("TEST!!!!",file=sys.stderr)
        if fileform.validate_on_submit():
            f = fileform.filefield.data
            filename = secure_filename(f.filename)
            print("Got file {}".format(filename), file=sys.stderr)
            if allowed_file(filename):
                filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                print("Saving output to {}".format(filepath), file=sys.stderr)
                f.save(filepath)
                upload_images_from_catalogue(filepath)
                return render_template("admin/uploaded.html",filename=filename)
    return render_template("admin/upload.html",form=fileform)
