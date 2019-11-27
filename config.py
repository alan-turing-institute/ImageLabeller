
"""
Configuration for image labeller app
"""

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    DB_TYPE = os.environ.get("DB_TYPE") or "sqlite3"
    if DB_TYPE == "sqlite3":
        SQLALCHEMY_DATABASE_URI = "sqlite:///{filepath}".format(
            filepath=os.path.join(
                BASEDIR, os.environ.get("SQL3_FILENAME") or "app.db"
            )
        )
    else:
        if DB_TYPE == "mysql":
            dbstring =  "mysql+pymysql"
        elif DB_TYPE == "postgres":
            dbstring = "postgres+psycopg2"
        else:
            dbstring = DBTYPE
        SQLALCHEMY_DATABASE_URI = "{dbstring}://{username}:{password}@{host}:{port}/{database}".format(
            dbstring = dbstring,
            username=os.environ.get("IL_DB_USER"),
            password=os.environ.get("IL_DB_PASSWORD"),
            host=os.environ.get("IL_DB_HOST"),
            port=os.environ.get("IL_DB_PORT"),
            database=os.environ.get("IL_DB_DATABASE"),
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    IMAGE_DIR = "static/images"
    IMAGE_FULLPATH = os.path.join(BASEDIR, IMAGE_DIR)

    CATEGORIES = ["Gaps",
                  "Labyrinths",
                  "Spots",
                  "None"]
    TITLE = "Image labeller"
    HOMEPAGE_TEXT = "Label vegetation patterns"
    TMPDIR = "/tmp/"
