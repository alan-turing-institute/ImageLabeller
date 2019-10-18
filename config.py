
"""
Configuration for image labeller app
"""

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    DB_TYPE = os.environ.get("DB_TYPE") or "sqlite3"
    if DB_TYPE == "mysql":
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(
            username=os.environ.get("IL_MYSQL_USER"),
            password=os.environ.get("IL_MYSQL_PASSWORD"),
            host=os.environ.get("IL_MYSQL_HOST"),
            port=os.environ.get("IL_MYSQL_PORT"),
            database=os.environ.get("IL_MYSQL_DATABASE"),
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///{filepath}".format(
            filepath=os.path.join(
                BASEDIR, os.environ.get("SQL3_FILENAME") or "app.db"
            )
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    IMAGE_DIR = "static/images"
    IMAGE_FULLPATH = os.path.join(BASEDIR, IMAGE_DIR)

    CATEGORIES = ["Gaps",
                  "Labyrinths",
                  "Spots",
                  "None"]
