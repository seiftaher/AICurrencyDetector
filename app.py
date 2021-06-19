#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import cv2
import numpy
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
import logging
from logging import Formatter, FileHandler
from IPModule import detectImage

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():

    return render_template('forms/search_image.html')


@app.route('/', methods=['POST'])
def search_image_post():
    currency = request.form.get('currency')

    if 'file' not in request.files:
        print("here")
        flash('No file part')
        return render_template('forms/search_image.html')
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return render_template('forms/search_image.html')
    if file:
        img = cv2.imdecode(numpy.fromstring(
            request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
        currencies, converted = detectImage(img, currency)

    return render_template('forms/search_image.html', image=True, currencies=currencies, converted=converted, currency=currency)

#----------------------------------------------------------------------------#
# Error Handler.
#----------------------------------------------------------------------------#


@app.errorhandler(404)
def not_found_error(error):
    print(error)
    return render_template('errors/404.html'), 404


@app.errorhandler(400)
def not_found_error(error):
    print(error)
    return render_template('errors/404.html'), 400


@app.errorhandler(500)
def server_error(error):
    print(error)
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
