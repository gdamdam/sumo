# class analyzer
# analyze a text returning some stats and Most_Freq_Words

import nltk
import string
import numpy
import re

from nltk.stem.porter import *
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from tools import tokenizer 
from tools import sum_luhn
from tools import summary 

N_MOST_FREQ_WORDS = 20	#number of returned most freq words

N = 170 # number of words to consider

class Analyzer():
	"""Class to analyzer the text
	"""

	# inizializing the Analyzer object
	def __init__(self,txt):
		self.sentences = 0
		self.words = 0
		self.unique_words = 0
		self.hapaxes = 0
		self.most_freq_words = []
		self.most_freq_stem_words = []
		self.most_freq_stem_words_wn = []
		self.entities = {}

		self._process(txt)


	def _process(self,txt):
		""" The function process the text and returning the results in the class object

		Args:
		  txt: input text to be analyzed.

		Returns: True
		"""
		self.lang = self.detect_lang(txt)
		words = []
		stemmed_words = []
		stemmed_words_wordnet = []


		if self.lang != '':
			stop_words = nltk.corpus.stopwords.words(self.lang)
			try:
				stemmer = SnowballStemmer(self.lang,ignore_stopwords=True)
			except:	
				print "WARNING: the Snowball stemmer is not supporting the detected language. Assuming english."
				stemmer = SnowballStemmer("english",ignore_stopwords=True)
		else:
			print "WARNING: no detected language. Assuming english."
			stop_words = nltk.corpus.stopwords.words('english')


		self.STOP_WORDS = stop_words+list(string.punctuation)+['``','\'\'','\'s','--']

		# tokenizing sentences - EOS detection
		sentences = tokenizer.get_sentences(txt)
		self.sentences = len(sentences)

		# tokenizing words
		words = tokenizer.get_words(sentences)

		# extract most freq words
		self.most_freq_words = self.get_most_freq_words(words,type='original')


		# extract most freq words in a stemmed words list using SnowBall stemmer
		# and filtering here the stop words
		for w in words:
			if w not in self.STOP_WORDS:
				stemmed_words.append(stemmer.stem(w))

		self.most_freq_stem_words = self.get_most_freq_words(stemmed_words,type='stemmed')


		# extract most freq words in a stemmed words list using WordNetLemmatizer
		# and filtering here the stop words
		lmtz = WordNetLemmatizer()
		for w in words:
			if w not in self.STOP_WORDS:
				stemmed_words_wordnet.append(lmtz.lemmatize(w))

		self.most_freq_stem_words_wn = self.get_most_freq_words(stemmed_words_wordnet,type='stemmed')



		# extracting and savint the Entities
		self.entities = self.get_entities(sentences)

		# extracting the two Luhn summaries
		self.summary_top_n, self.summary_mean_scored = sum_luhn.summarize(sentences,self.STOP_WORDS)		

		# extractin intersection summery
		self.abs_summary = summary.Summary(txt)
		return 1



	def get_most_freq_words(self,words,type):
		""" Function receive a word list and return a list with the N most freq words

		Args:
		  words: the words list
		  type: define if the words list is the original one or a stemmed one
		
		Returns:
		  a list with the N_MOST_FREQ_WORDS most frequent words
		"""
		most_freq_words = []
		words_cleaned = []

		## doing some custom cleaning for some text very bad formatted
		for w in words:
			words_cleaned.append(re.sub(r'\.', ' ', w))

		# getting the words frequency distribution
		fdist = nltk.FreqDist(words_cleaned)

		# saving the words counts only with the full words list
		if type == 'original':
			self.words = sum([i[1] for i in fdist.items()])
			self.unique_words = len(fdist.keys())

			# Hapaxes are words that appear only once
			self.hapaxes = len(fdist.hapaxes())

		words_no_stop = dict([w for w in fdist.items() if w[0] not in self.STOP_WORDS])


		# ordering the results
		keys_most_freq_words = sorted(words_no_stop, key=words_no_stop.__getitem__, reverse=True)

		for k in keys_most_freq_words:
				if len(k)>1:
					most_freq_words.append((k,words_no_stop[k])) 
	
		# return the result in ordered list
		return most_freq_words[:N_MOST_FREQ_WORDS]



	def detect_lang(self,text):
		""" Returns the detected language.

		Args:
		  text: input text 

		Returns:
		  the detectred language string
		"""
		language_ratio = {}
		words = wordpunct_tokenize(text)

		for language in stopwords.fileids():
			stopwords_set = set(stopwords.words(language))
			words_set = set(words)
			common_words = words_set.intersection(stopwords_set)
			language_ratio[language] = len(common_words)

		detected_lang = max(language_ratio, key=language_ratio.get)

		return detected_lang


	def stemmer(self,word):
		""" Returns the stemmed version of the input word using a Porter Stemmer.
		"""
		stemm = PorterStemmer()
		return stemm.stem(word)


	def get_entities(self,sentences):
		""" The function returns the dictionary containing the results for
		the Name Entity Recognition analyze.

		Args:
		   sentences: the sentences list.

		Returns:
			dictionary:
		"""
		entities = dict([])

		# Tokenization
		tokens = [nltk.tokenize.word_tokenize(s) for s in sentences]

		# Part-Of-Speech tagging
		pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]

		# Chunking
		chunked_nes = [nltk.ne_chunk(c) for c in pos_tagged_tokens]

		for tree in chunked_nes:
			for s in tree.subtrees(lambda t: (t.height()==2)):
				if s.label()!='S':
					entity = ' '.join(i[0] for i in s.leaves())
					if s.label() in entities.keys():
						if entity not in entities[s.label()]:
							entities[s.label()].append(entity)
							entities[s.label()].sort()
					else:	
						entities[s.label()] = [entity]

		return entities




		


if __name__ == "__main__":
        main()	
