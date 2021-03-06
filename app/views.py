from flask import * #TODO: actually look at imports
import boto3
import requests
import json
import urllib
from werkzeug import * #TODO: actually look at imports
import classify as watson
import news

views = Blueprint('views', __name__)

extensions = set(['jpg'])

def file_allowed(file):
	return '.' in file and \
			 file.rsplit('.', 1)[1] in extensions

@views.route('/', methods=["GET", "POST"])
def homepage():
	if request.method == "POST":
		return render_template('homepage.html', sunalt=news.timeline(request.form.get('stock')))
	else:
		return render_template('homepage.html', sunalt=None)

@views.route('/about')
def about():
	return render_template('about.html')


# def ocr_space_file(filename, overlay=False, api_key='6960bb930988957', language='eng'):
#     """ OCR.space API request with local file.
#         Python3.5 - not tested on 2.7
#     :param filename: Your file path & name.
#     :param overlay: Is OCR.space overlay required in your response.
#                     Defaults to False.
#     :param api_key: OCR.space API key.
#                     Defaults to 'helloworld'.
#     :param language: Language code to be used in OCR.
#                     List of available language codes can be found on https://ocr.space/OCRAPI
#                     Defaults to 'en'.
#     :return: Result in JSON format.
#     """

#     payload = {'isOverlayRequired': overlay,
#                'apikey': api_key,
#                'language': language,
#                }
#     with open(filename, 'rb') as f:
#         r = requests.post('https://api.ocr.space/parse/image',
#                           files={filename: f},
#                           data=payload,
#                           )
#     return r.content.decode()


# def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
#     """ OCR.space API request with remote file.
#         Python3.5 - not tested on 2.7
#     :param url: Image url.
#     :param overlay: Is OCR.space overlay required in your response.
#                     Defaults to False.
#     :param api_key: OCR.space API key.
#                     Defaults to 'helloworld'.
#     :param language: Language code to be used in OCR.
#                     List of available language codes can be found on https://ocr.space/OCRAPI
#                     Defaults to 'en'.
#     :return: Result in JSON format.
#     """

#     payload = {'url': url,
#                'isOverlayRequired': overlay,
#                'apikey': api_key,
#                'language': language,
#                }
#     r = requests.post('https://api.ocr.space/parse/image',
#                       data=payload,
#                       )
#     return r.content.decode()


