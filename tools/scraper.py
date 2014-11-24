import StringIO
import gzip
import urllib2
import re

from goose import Goose

from tools import tokenizer 
from tools import analyzer
from tools import summary 



def _get_html_content_from_url(URL):
	"""
	Returns the content page of the given URL.
	"""

	#hdr = {'User-Agent': 'Mozilla/5.0'}
	request = urllib2.Request(URL)
	#request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)


	if response.info().get('Content-Encoding') == 'gzip':
		print "Content-Encoding: gzip"
		print "unzippinig....."
		buf = StringIO.StringIO(response.read())
		f = gzip.GzipFile(fileobj=buf)
		return f.read(),response.info().type
	else:
		print "the content seems uncompressed"
		return response.read(),response.info().type


def extract(URL):
	"""
	This function extract the page's text body of the given URL.

	Return:
		page_title: the value of the <title> html tag
		text_extracted: the extracted body text
		img: top_image url extracted
	"""

	g = Goose()

	text, text_type= _get_html_content_from_url(URL)

	if text_type != 'text/plain':
	#article = g.extract(url=URL)
		article = g.extract(raw_html=text)

		img = ''

		try:
			img = article.top_image.src
		except:
			img = ''
		return (article.title,article.cleaned_text,img)
	else:
		print "it's a plain/text"
		return ('plaintext',text,'n/a')


def get_simple_html(txt):
	text = re.sub(r'\n', '<br>', txt)
	return text


# highlight the sentences into txt
def get_highlight(txt,sentences):
	"""Function to highlight the sentences into a text.

	Args:
		txt: the full text.
		sentences: a list of all the sentences to highlight.

	Returns:
		the text string html formatted
	"""
	text = ''
	all_sent = tokenizer.get_sentences(txt)
	for sent in all_sent:
		if sent in sentences:
			text += " <b>"+sent+"</b> "
		else:
			text += sent

	return text


## the function return a dictionary with all the data scraped from the text
##
def get_scraped_data(page_title,text,img,URL):
	"""Function to scrap the data from a text.

	Args:
            page_title: a string with the page title value.
            text: the text to be scraped.
            URL: the URL string value

        Returns:
            the dictionary with all the data scraped form the text.
            check the code for the complete keys list.
	"""

	# analyzing the text
	anl = analyzer.Analyzer(text)

	# tring another sumarizing tool
	abs_summary = summary.Summary(text)

	# preparing the result
	result = {}
	result['page_title'] = page_title
	result['img'] = img
	result['url_name'] = normalize_url(URL)
	result['url'] = URL
	result['body'] = text
	result['lang'] = anl.lang
	result['sentences'] = anl.sentences
	result['words'] = anl.words
	result['unique_words'] = anl.unique_words
	result['hapaxes'] = anl.hapaxes


	result['most_freq_words'] = {}
	for k,v in anl.most_freq_words:
		result['most_freq_words'][k] = v

	result['most_freq_stem_words'] = {}
	for k,v in anl.most_freq_stem_words:
		result['most_freq_stem_words'][k] = v

	result['most_freq_stem_words_wn'] = {}
	for k,v in anl.most_freq_stem_words_wn:
		result['most_freq_stem_words_wn'][k] = v

	result['entities'] = {}
	for k,v in anl.entities.iteritems():
		result['entities'][k] = v

	result['summary'] = {}
	result['summary']['luhn2'] = anl.summary_top_n
	result['summary']['luhn1'] = anl.summary_mean_scored
	result['summary']['intersect'] = abs_summary.summary

	return result	


def normalize_url(url):
	"""Function to normalize the url. It will be used as document id value.

	Returns:
	  the normalized url string.
	"""
	norm_url = re.sub(r'http://', '', url)
	norm_url = re.sub(r'https://', '', norm_url)
	norm_url = re.sub(r'/', '__', norm_url)
	return norm_url



if __name__ == "__main__":
        main()
