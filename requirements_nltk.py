import nltk

TO_DOWNLOAD=['stopwords','punkt','wordnet','words','maxent_ne_chunker','maxent_treebank_pos_tagger']

for i in TO_DOWNLOAD:
	print i
	nltk.download(i)
