"""
Useful functions for the admin panel of ImageLabeller.  In particular:
* Download labels from database to json or csv
* Upload images to the database, from json (catalogue of image locations) or zip archive

NOTE:
When uploading files, or an archive full of files, we will attempt to
match the filename to a regex with longitute_latitude_date (with date in ISO3 format)
and upload those values to the database
"""

import os
import sys
import json
import re
from flask import current_app
from datetime import datetime

from image_labeller import db
from image_labeller.schema import Label, User, Image, Category

REGEX = "([\d]{1,3}\.[\d]+)_([\d]{1,3}\.[\d]+)_([\d]{4}-[0-1][\d]{1}-[0-3][\d]{1})"


def prep_data():
    """
    query the database label table and return results as a dict
    """
    all_results = []
    results = Label.query.all()
    print("We have {} results".format(len(results)))
    for result in results:
        result_dict = {}
        result_dict["image_name"] = result.image.image_location
        result_dict["username"] = result.user.username
        result_dict["category"] = result.category.category_name
        result_dict["notes"] = result.notes
        if result.image.image_longitude:
            result_dict["longitude"] = result.image.image_longitude
        if result.image.image_latitude:
            result_dict["latitude"] = result.image.image_latitude
        if result.image.image_time:
            dt = result.image.image_time
            # convert datetime to a string
            if isinstance(dt, datetime):
                dt = dt.isoformat().split("T")[0]
            result_dict["time"] = dt
        all_results.append(result_dict)
    return all_results


def prep_csv(filename, tmpdir):
    """
    write a CSV file to temp dir
    """
    if not filename.endswith(".csv"):
        filename += ".csv"
    results = prep_data()
#    tmpdir = os.path.join(os.getcwd(), tmpdir)
    os.makedirs(tmpdir, exist_ok=True)
    tmp_filename = os.path.join(tmpdir, filename)
    tmp_file = open(tmp_filename, "w")
    # should be empty string if no results found
    headers = results[0].keys() if len(results)>0 else []
    first_line = ""
    for header in headers:
        first_line += header+","
    first_line = first_line[:-1]+"\n"
    tmp_file.write(first_line)
    for result in results:
        line = ""
        for header in headers:
            line += result[header] + ","
        line = line[:-1]
        tmp_file.write(line+"\n")
    return filename


def prep_json(filename, tmpdir):
    """
    write a json file to temp dir and return its location
    """
    if not filename.endswith(".json"):
        filename += ".json"
#    tmpdir = os.path.join(os.getcwd(), tmpdir)
    os.makedirs(tmpdir, exist_ok=True)
    tmp_filename = os.path.join(tmpdir, filename)
    results = prep_data()
    with open(tmp_filename,"w") as outfile:
        json.dump(results, outfile)
    return filename



def upload_image(image_dict):
    """
    Upload a single image to the database
    """
    if (not "image_location" in image_dict.keys()) or \
       (not "image_location_is_url" in image_dict.keys()):
        raise RuntimError("Need to specify image_location and image_location_is_url")
    img = Image()
#    print("Uploading image {}".format(image_dict["image_location"]),file=sys.stderr)
    img.image_location = image_dict["image_location"]
    img.image_location_is_url = image_dict["image_location_is_url"]
    for k in ["image_longitude","image_latitude","image_time"]:
        if k in image_dict.keys():
            img.__setattr__(k, image_dict[k])
    db.session.add(img)
    db.session.commit()



def upload_images_from_catalogue(catalogue_file):
    """
    Upload a set of images to the database - given a json file containing
    [{image_location:<loc>,image_location_is_url}, ...]
    """
    image_catalogue = json.load(open(catalogue_file))

    if (not isinstance(image_catalogue, list)) or \
       (not isinstance(image_catalogue[0], dict)):
        raise RuntimeError("upload_images needs to be given a list of dictionaries")
    for image_dict in image_catalogue:
        upload_image(image_dict)


def upload_images_from_archive(archive_file):
    """
    Unpack a zipfile or tarfile to the right directory,
    and upload details to the database.
    """
    # make a directory with the current timestamp name
    timestring = str(datetime.timestamp(datetime.now())).split(".")[0]

    # "upload_dir" is the absolute file path, where we will unzip files to.
    upload_dir = os.path.join(current_app.config["IMAGE_FULLPATH"],timestring)
    os.makedirs(upload_dir)
    # location_dir is the last part of this, to be used in the URL
    location_dir = os.path.join(current_app.config["IMAGE_PATH"],timestring)
    if archive_file.endswith(".zip"):
        os.system("unzip {} -d {}".format(archive_file, upload_dir))
    ## list the files in the directory
    filenames = os.listdir(upload_dir)
    for filename in filenames:
        image_dict = {}
        image_dict["image_location"] = os.path.join(location_dir,
                                                    filename)
        image_dict["image_location_is_url"] = False
        # see if we can extract latitude_longitude_date from the filename
        match = re.search(REGEX, filename)
        if match:
            longitude, latitude, date = match.groups()
            image_dict["image_latitude"] = latitude
            image_dict["image_longitude"] = longitude
            image_dict["image_time"] = date
        upload_image(image_dict)


def upload_images(filename):
    """
    Depending on the file extension upload either a zipfile of files
    to local disk, or a json of file locations (URLs).
    """
    if filename.lower().endswith(".json"):
        upload_images_from_catalogue(filename)
    elif filename.lower().endswith(".zip"):
        upload_images_from_archive(filename)
    else:
        print("Filetype not implemented yet")



def allowed_file(filename):
    """
    Check an uploaded filename is of an allowed type.
    """
    allowed_extensions = {'.json', '.zip', '.png'}
    for ext in allowed_extensions:
        if filename.endswith(ext):
            return True
    return False
