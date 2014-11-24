# Sumo 
An API for semantic analysis of web articles.


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

## Start

Just lunch the server

<pre>
python ./sumo_server.py -s <IP>
</pre>

for help and all the options you can use
<pre>
python ./sumo_server.py --help
</pre>

The server provides a REST resource for analyze and store the analysis data of a web document.

## API Usage

The following comand returns the <b>list of all the documents stored</b>
<pre>
curl http://host:5000/sumo
</pre>

The stored documents are labeled with a <ID_DOC>, where the \/ caracter in the URL
are substitued with \_\_
<pre>
	URL: www.google.com/test
 ID_DOC: www.google.com__test
</pre>

<b>To analyze and store a document</b> and store it on the db:
<pre>
curl http://host:5000/sumo -X POST -d "url=<TARGET_URL>"
</pre>
HTTP Status returned:
<pre>
	201:	Created		- the document at <TARGET_URL> sucessfully analyzed and stored
	409:	Conflict	- if the <TARGET_URL> already exists in the storade
	415:	Unsupported	- the TARGET_URL is malformed
</pre>

<b>To retrieve a stored document</b> analysis:
<pre>
curl http://host:500/sumo/<ID_DOC>
</pre>
HTTP Status returned:
<pre>
	200:	OK			
	404:	Not Found 	- the document does not exist
</pre>

<b>To delete a stored document</b>:
<pre>
curl http://host:500/sumo/<ID_DOC> -X DELETE
</pre>
HTTP Status returned:
<pre>
	204:	No Content	- document deleted 
	404:	Not Found 	- the document does not exist
</pre>

It is possible <b>retrieve the cluster</b> of similar documents using the cluster resource
<pre>
curl http://host:500/sumo/cluster/<ID_DOC>
</pre>
HTTP Status returned:
<pre>
	200:	OK
	404:	Not Found 	- the document does not exist
</pre>


## Web Interface

The running server provides also a very minimal javascript web interface to interact with the API.
The interface is reacheable at:
<pre>
http://host:port
</pre>

Tips:
- single click on an id in the index to fill the form and click analyze to retrieve the analysis.
- double click on an id in the index to delete it.
