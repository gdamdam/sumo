import nltk
import string

# sentence tokenizer
def get_sentences(txt):
	""" Returns the sentences tokenization of the given text.
	
	Args: 
	  txt: the input text string.

	Returns:
	  list. 
	"""
	return nltk.tokenize.sent_tokenize(txt)


# word tokenizer
def get_words(sentences):
	""" Returns the word tokenization of the given sentences list.

	Args:
	  sentences: sentences list

	Returns:
	  list. """
	return [w.lower() for sentence in sentences for w in nltk.tokenize.word_tokenize(sentence)]
	

# paragraph tokenizer
def get_paragraphs(txt):
	""" Returns the paragraphs list of the given text.
	
	Args:
	  txt: the input text string.

	Returns: 
	  list. """
	return txt.split(".\n")





if __name__ == "__main__":
    main()