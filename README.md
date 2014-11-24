# Sumo 
a tool for semantic analysis of web articles.


## Main requirements
<pre>
MongoDB >=2.6.5 
Python >=2.7.5
</pre>

## Basic Installation

<pre>
git clone https://github.com/gdamdam/sumo.git
cd sumo
pip install -r requirements.txt
python requirements_nltk.py
</pre>

## Usage
Just lunch the server

<pre>
python ./sumo_server.py
</pre>

the server provides a REST resource for analyze and store the analysis data of a web document.

The following comand returns the list with all the documents sotred
<pre>
curl http://host:5000/sumo
</pre>

The stored documents are labeled with a <ID_DOC>, where the \/ caracter in the URL
are substitued with \_\_
<pre>
	URL: www.google.com/test
 ID_DOC: www.google.com__test
</pre>

To analyze a document and store the results on the db:
<pre>
curl http://host:5000/sumo -X POST -d "url=<TARGET_URL>"
</pre>
HTTP Status returned:
<pre>
	201:	Created		- the document at <TARGET_URL> sucessfully analyzed and stored
	409:	Conflict	- if the <TARGET_URL> already exists in the storade
	415:	Unsupported	- the TARGET_URL is malformed
</pre>

To retrieve a stored document analysis:
<pre>
curl http://host:500/sumo/<ID_DOC>
</pre>
HTTP Status returned:
<pre>
	200:	OK			
	404:	Not Found 	- the document does not exists
</pre>

To delete a stored document:
<pre>
curl http://host:500/sumo/<ID_DOC> -X DELETE
</pre>
HTTP Status returned:
<pre>
	204:	No Content	- document deleted 
	404:	Not Found 	- the document does not exists
</pre>

It is possible retrieve the cluster of similar documents using the cluster resource
<pre>
curl http://host:500/sumo/cluster/<ID_DOC>
</pre>
HTTP Status returned:
<pre>
	200:	OK
	404:	Not Found 	- the document does not exists
</pre>

