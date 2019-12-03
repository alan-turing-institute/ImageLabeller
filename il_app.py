"""
Simple flask app for labelling images.

"""
import time

from image_labeller import create_app


if __name__ == "__main__":
    time.sleep(5) # wait for postgres server to start

    app = create_app()
    app.run(host='0.0.0.0',port=5000, debug=True)
