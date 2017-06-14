## This module contains the function to interact with the mongodbimport sys
import datetime
import sys
from pymongo import Connection
from pymongo.errors import ConnectionFailure



def _mongo_connect():
	""" Internal function to connect to the mongodb	"""
	# making connection with mongodb	
	try:
		con = Connection(host='localhost', port=27017)
	except ConnectionFailure, e:
		sys.stderr.write("Could not connect to mongodb: %s" % e)
		sys.exit(1)
	# getting the database hande
	dbh = con['sumo']

	assert dbh.connection == con

	return dbh


## this function insert an article object into the mongodb##
def mongo_insert(article_obj):
	""" The function inserts an article object in the mongo dbh	
        
        Args:
	    article_obj: aticle object

	Returns: True
	"""	

	# connect to mongo
	dbh = _mongo_connect()

	# getting the articles collection
	articles = dbh.articles

	# inserting article 
	article_obj['date_insert'] = str(datetime.datetime.now())
	articles.insert(article_obj)

	dbh.connection.close()
	return 1

def mongo_remove(query):
	""" The function delete a document form the mongodg

	Args:
	    query: the article url_name to remove

	Returns: True
	"""
	# connect to mongo
	dbh = _mongo_connect()

	# getting the articles collection
	articles = dbh.articles

	# inserting article 
	articles.remove({'url_name':query})
	dbh.connection.close()

	return 1


def mongo_find(query):
	""" The function process the text and returning the results in the class object

	Args:
		query: the url_name of the document 

	Returns: 
		doc: the document found
	"""
	# connect to mongo
	dbh = _mongo_connect()

	# getting the articles collection
	articles = dbh.articles	

	document = articles.find_one({'url_name':query})

	## removing the mongodb bson _id 
	doc = document
	del doc['_id']
	dbh.connection.close()

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
#	dbh = _mongo_connect()
#
#	articles = dbh.articles
#
#	articles.update({'url_name':query},{"$set":{'analysis':analysis_results}})
#
#	return 1





def mongo_all(result_num):
	""" The function return rest_nums documents for the dbh	Args:
		resuts_num: the number of results to show

	Returns: 
		resuts: the results set
	"""	
	# connect to mongo
	dbh = _mongo_connect()

	# getting the articles colletions
	articles = dbh.articles

	# find the document
	documents = articles.find().limit(result_num)

	i = 0
	results = {}

	for document in documents:
		i += 1
		results[i] = document['url_name']

	dbh.connection.close()
	return results



## the main
##
def main():
	pass



if __name__ == "__main__":
    main()
