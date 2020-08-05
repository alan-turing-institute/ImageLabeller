# ImageLabeller
Simple Flask app to allow users to label images and save results in a database.  Can be run either via *docker-compose* or directly. 
For deploying as a web-app, we recommend the *docker-compose* option - see instructions for this here.

## Running with Docker(compose)

If you have Docker and docker-compose installed, just run the commands
```
docker-compose build
docker-compose up
```
Then point your browser to `localhost:80/`.

## Requirements for running locally (native)

It is recommended to use a virtualenv or conda environment to run this, in order to avoid the risk of clashes with other python packages.
```
pip install -r requirements.txt
```

## Run the flask app

From this directory, run
```
python il_app.py
```
Then navigate your browser to ```http://localhost:5000```

## Upload data

First, put the data you want to load into a zip archive.
* Put all the files into a single directory and `cd` to that directory.
* Do ```zip -f <zipfilename> .``` - it is recommended that you name the zipfile with "<longitude>_<latitude>_<YYYY-MM-DD>" in the filename to enable the coordinates and date to be inferred and saved along with the image.
* Login to *ImageLabeller* as an admin user, and go to the base URL plus ```/admin/upload``` then select your zipfile and click "Save".


## Retrieve the data

If you are a user with `admin` rights, navigate to ```http://localhost:5000/admin/download``` to retrieve the assigned labels as a .csv or .json file.
