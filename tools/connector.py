## This module contains the function to interact with the mongodb

import datetime
from pymongo import MongoClient



def _mongo_connect():
	""" Internal function to connect to the mongodb
	"""
	# making connection with mongodb
	client = MongoClient('localhost', 27017)

	# getting the sumo database
	db = client.sumo

	return db



## this function insert an article object into the mongodb
##
def mongo_insert(article_obj):
	""" The function inserts an article object in the mongo db

	Args:
	article_obj: aticle object

	Returns: True
	"""	

	# connect to mongo
	db = _mongo_connect()

	# getting the articles collection
	articles = db.articles

	# inserting article 
	article_obj['date_insert'] = str(datetime.datetime.now())
	articles.insert(article_obj)

	return 1

def mongo_remove(query):
	""" The function delete a document form the mongodg

	Args:
		query: the article url_name to remove

	Returns: True
	"""
	# connect to mongo
	db = _mongo_connect()

	# getting the articles collection
	articles = db.articles

	# inserting article 
	articles.remove({'url_name':query})

	return 1


def mongo_find(query):
	""" The function process the text and returning the results in the class object

	Args:
		query: the url_name of the document 

	Returns: 
		doc: the document found
	"""
	# connect to mongo
	db = _mongo_connect()

	# getting the articles collection
	articles = db.articles	

	document = articles.find_one({'url_name':query})

	## removing the mongodb bson _id 
	doc = document
	del doc['_id']

	return doc


#def mongo_append(query,analysis_results):
#	""" The function append the data to the document
#
#	Args:
#		query: the url_name to find and update
#		analysis_results: the data object to append
#
#	Returns: True
#	"""
#
#	db = _mongo_connect()
#
#	articles = db.articles
#
#	articles.update({'url_name':query},{"$set":{'analysis':analysis_results}})
#
#	return 1





def mongo_all(result_num):
	""" The function return rest_nums documents for the db

	Args:
		resuts_num: the number of results to show

	Returns: 
		resuts: the results set
	"""	
	# connect to mongo
	db = _mongo_connect()

	# getting the articles colletions
	articles = db.articles

	# find the document
	documents = articles.find().limit(result_num)

	i = 0
	results = {}

	for document in documents:
		i += 1
		results[i] = document['url_name']

	return results



## the main
##
def main():
	pass



if __name__ == "__main__":
    main()
