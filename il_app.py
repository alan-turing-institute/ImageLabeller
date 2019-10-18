"""
Simple flask app for labelling images.

"""

from image_labeller import create_app


if __name__ == "__main__":

    app = create_app()
    app.run(host='0.0.0.0',port=5000, debug=True)
