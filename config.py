
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
            username=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_DATABASE"),
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False

######## use Flask-Mail to send confirmation-request or password-reset mails

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_ADMIN = os.environ.get("ADMIN_EMAIL")


######### admin user added to user table when app is first started

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

####### storage of uploaded images or catalogues

    UPLOAD_FOLDER = "/tmp/"


###### Application-specific

    IMAGE_DIR = "static/images"
    IMAGE_FULLPATH = os.path.join(BASEDIR, IMAGE_DIR)

    CATEGORIES = ["Gaps",
                  "Labyrinths",
                  "Spots",
                  "None"]
    TITLE = "Image labeller"
    HOMEPAGE_TEXT = "Label vegetation patterns"
    TMPDIR = "/tmp/"
