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

N_MOST_FREQ_WORDS = 20			#number of returned most freq words

N = 170 # number of words to consider
CLUSTER_THRESHOLD = 5 #distance between words to consider
TOP_SENTENCES = 5 # number of sentences to return for a "top n" summary

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
		# THIS IS THE STEP USING THE COMPLETE WORD LIST
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

		# extract most freq stemmed words using WordNet Lemmatizer
		self.most_freq_stem_words_wn = self.get_most_freq_words(stemmed_words_wordnet,type='stemmed')



		## extracting and savint the Entities
		self.entities = self.get_entities(sentences)

		## extracting the two Luhn summaries
		##
		self.summary_top_n, self.summary_mean_scored = self.summarize(sentences)		

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




#### REVIEW THIS CODE
#### Add the source reference and credits
		#The functions returns two summary using Luhn Algorithms

		#Args:
		#  sentences: the sentences list.

		#Returns:
		#  top_n_summary: dictionary with the sentences part of the summary
		#  mean_scored_summary: dictionary with the sentences part of the summary 
		
	def summarize(self,sentences):

	    normalized_sentences = [s.lower() for s in sentences]

	    words = [w.lower() for sentence in normalized_sentences for w in nltk.tokenize.word_tokenize(sentence)]
	    words = [word for word in words if word not in self.STOP_WORDS]

	    fdist = nltk.FreqDist(words)

	    words_dist = dict(fdist.items())
	    keys_most_freq_words = sorted(words_dist, key=words_dist.__getitem__, reverse=True)

	    top_n_words = []
	    for k in keys_most_freq_words:
	    	top_n_words.append(k)		


	    scored_sentences = self._score_sentences(normalized_sentences, top_n_words[:100])


	    ### Summarization with Luhn Algorithm 

	    # Approach 1:
	    # Filter out nonsignificant sentences by using the average score plus a
	    # fraction of the std dev as a filter
	    avg = numpy.mean([s[1] for s in scored_sentences])
	    std = numpy.std([s[1] for s in scored_sentences])
	    mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences if score>avg+0.5*std]


        # Summarization Approach 2:
        # Another approach would be to return only the top N ranked sentences
	    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-TOP_SENTENCES:] 
	    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])

	        # Decorate the post object with summaries
	    res = dict(top_n_summary=[sentences[idx] for (idx, score) in top_n_scored], mean_scored_summary=[sentences[idx] for (idx, score) in mean_scored])

	    return res['top_n_summary'],res['mean_scored_summary']




	def _score_sentences(self, sentences, important_words):
	    scores = []
	    sentence_idx = -1

	    for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:
	        sentence_idx += 1
	        word_idx = []

	        # for each word in the word list
	        for w in important_words:
	            try:
	                # compute index for where any important words occur in the sentence
	                word_idx.append(s.index(w))
	            except ValueError, e:
	                pass

	        word_idx.sort()
	        # some sentences may have not contain any important words at all.
	        if len(word_idx) == 0: continue

	        # using the word index, compute clusters by using a max distance threshold for any two consecutive words.
	        clusters = []
	        cluster = [word_idx[0]]
	        i = 1
	        while i < len(word_idx):
	            if word_idx[i]- word_idx[i-1] < CLUSTER_THRESHOLD:
	                cluster.append(word_idx[i])
	            else:
	                clusters.append(cluster[:])
	                cluster = [word_idx[i]]
	            i += 1
	        clusters.append(cluster)

	        #score each cluster. the max score for any given clustr is the score for the sentence.
	        max_cluster_score = 0
	        for c in clusters:
	            significant_words_in_cluster = len(c)
	            total_words_in_cluster = c[-1]-c[0]+1
	            score = 1.0 * significant_words_in_cluster \
	                    * significant_words_in_cluster/total_words_in_cluster

	            if score > max_cluster_score:
	                max_cluster_score = score

	        scores.append((sentence_idx, score))

	    return scores

if __name__ == "__main__":
        main()	