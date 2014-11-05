"""
Copyright (c) 2013, Matthew A. Russell
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
"""
from __future__ import division

import nltk
import numpy

TOP_SENTENCES = 5 # number of sentences to return for a "top n" summary
CLUSTER_THRESHOLD = 5 #distance between words to consider


def summarize(sentences,STOP_WORDS):
    normalized_sentences = [s.lower() for s in sentences]

    words = [w.lower() for sentence in normalized_sentences for w in nltk.tokenize.word_tokenize(sentence)]
    words = [word for word in words if word not in STOP_WORDS]

    fdist = nltk.FreqDist(words)

    words_dist = dict(fdist.items())
    keys_most_freq_words = sorted(words_dist, key=words_dist.__getitem__, reverse=True)

    top_n_words = []
    for k in keys_most_freq_words:
    	top_n_words.append(k)		


    scored_sentences = _score_sentences(normalized_sentences, top_n_words[:100])


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




def _score_sentences(sentences, important_words):
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