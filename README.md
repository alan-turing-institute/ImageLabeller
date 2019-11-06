# ImageLabeller
Simple Flask app to allow users to label images and save results in a database

## Requirements

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

## Retrieve the data

If you are a user with `admin` rights, navigate to ```http://localhost:5000/admin/download``` to retrieve the assigned labels as a .csv or .json file.
