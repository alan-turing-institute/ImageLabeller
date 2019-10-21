"""
Useful functions for the admin panel of ImageLabeller
"""

import os
import json
from image_labeller.schema import Label, User, Image, Category


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
