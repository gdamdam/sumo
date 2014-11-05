# class summary to summaryze a given text through intersection
from __future__ import division

import nltk
import string
import numpy
from nltk.stem.porter import *
from tools import tokenizer 


#
# code forked from
# https://gist.github.com/shlomibabluki/5473521
# Created by Shlomi Babluki
# April, 2013

class Summary():

    def __init__(self,txt):
        self.summary = self.get_summary(txt)


    def sentences_intersection(self,sent1,sent2):

        # vectors sentences
        s1 = set(sent1.split(' '))
        s2 = set(sent2.split(' '))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        dist = (float(len(s1.intersection(s2))) / (float((len(s1) + len(s2))) / 2))

        # Normalize the result by the average number of words
        return dist


    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def clean_sentence(self,sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence


    # convert the text into a dictionary <key: formatted sentence, value: rank of the sentence>
    def get_sentence_ranks(self,txt):

        sentences = tokenizer.get_sentences(txt)

        # intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])
         
        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.clean_sentence(sentences[i])] = score
        return sentences_dic


    def get_best_sentence(self,paragraph,sentences_dic):
        sentences = tokenizer.get_sentences(paragraph)

        # ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.clean_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence


    def get_summary(self,txt):
        summary = []
        # get paragraph
        paragraphs = tokenizer.get_paragraphs(txt)
        
        # build the sentences dictionary
        sentences_dic = self.get_sentence_ranks(txt)

        # add to the summary the best sentence frome ach paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p,sentences_dic).strip()
            if sentence :
                summary.append(sentence)

        return summary



if __name__ == "__main__":
        main()