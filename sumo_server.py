"""
The MIT License

Copyright (c) 2014 Giovanni Damiola & Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from flask import Flask, jsonify, render_template, url_for
from flask.ext.restful import reqparse, abort, Api, Resource
from flask_bootstrap import Bootstrap

import re
import json
from bson import json_util

from tools import connector
from tools import scraper
from tools import clusterizer



app = Flask(__name__)
Bootstrap(app)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('url', type=str)


## fucntion to check if the entry already exists
def it_exists(url):
	try:
		url_norm = scraper.normalize_url(url)
		print url
		print url_norm
		if len(connector.mongo_find(url_norm)) > 0:
			return 1
		else:
			return 0
	except:
		print "...this is the first entry?"
		return 3


## check if the string is a valid url
def it_is_url(url):
	regex = re.compile(
        r'^https?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	if re.match(regex,url):
		return True
	else:
		return False

##### Main page
#####
@app.route('/')
def index():
	url_for('static', filename='style.css')
	url_for('static', filename='favicon.ico')
	url_for('static', filename='jquery.tagcloud.js')
	return render_template('main.html')


##### Sumo REST API initialization

##	show a list of documents and lets you POST to add new documents
class Sumo(Resource):

	# GET : retrieve the documents index from mongodb 
    def get(self):
        return connector.mongo_all(1000), 200

    # POST : analyze the submitted document and save the results on mongodb
    def post(self):
		args = parser.parse_args()
		url = args['url']
		if it_is_url(url):
			if it_exists(url) == 1:
				abort(409, message = "CONFLICT The document {} already exists".format(url))
			else:
				page_title, text, img = scraper.extract(url)
				result = scraper.get_scraped_data(page_title,text,img,url)
				connector.mongo_insert(result)
				return {"CREATED":url},201
		else:
			return {"MALFORMED URL":url},415


## resource for retrieve the documents
##
class SumoDocument(Resource):

	# GET : retrieve the results for the document requested
	def get(self,url_norm):
		if it_exists(url_norm) == 1:
			result = connector.mongo_find(url_norm)
			return result, 200
		else:
			abort(404, message = "NOT FOUND: The document {} doesn't exists".format(url_norm))
		return url

	# DELETE : remove the document requested from mongodb
	def delete(self,url_norm):
		if it_exists(url_norm) == 1:
			result = connector.mongo_remove(url_norm)
			return result, 204
		else:
			abort(404, message = "NOT FOUND: The document {} doesn't exists".format(url_norm))
		return url	


# resource to retrieve the document cluster
class SumoCluster(Resource):

	# GET : retrieve the cluster for the document requested
	def get(self,url_norm):
		if it_exists(url_norm) == 1:
			cluster = clusterizer.get_cluster(url_norm)
			print "WARNING: clustering in real time, consider a solution usin a db for partial results"
			return cluster, 200
		else:
			abort(404, message = "NOT FOUND: The document {} doesn't exists".format(url_norm))
		return url




# Initializing the api resources

api.add_resource(Sumo, '/sumo')
api.add_resource(SumoDocument, '/sumo/<string:url_norm>')
api.add_resource(SumoCluster, '/sumo/cluster/<string:url_norm>')




if __name__ == '__main__':
    app.run(debug=True, host='46.4.206.92')
