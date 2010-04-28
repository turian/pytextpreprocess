#!/usr/bin/python

import common.html2text
import common.tokenizer

from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
#from nltk.corpus import stopwords

import os.path
import re
import string

STOPFILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "english.stop")
stoplist = [string.strip(l) for l in open(STOPFILE).readlines()]

def textpreprocess(txt, converthtml=True, sentencetokenize=True, removeblanklinks=True, wordtokenize=True, lowercase=True, removestopwords=True, stem=True):
    """
    Note: For html2text, one could also use NCleaner (common.html2text.batch_nclean)
    Note: One could improve the sentence tokenization, by using the
    original HTML formatting in the tokenization.
    Note: We use the Porter stemmer. (Optimization: Shouldn't rebuild
    the PorterStemmer object each time this function is called.)
    """
    if converthtml:
        txt = common.html2text.html2text(txt)

    if sentencetokenize:
        txts = common.tokenizer.tokenize(txt)
    else:
        txts = [txt]
    txt = None

    if removeblanklinks:
        newtxts = []
        for t in txts:
            if len(string.strip(t)) > 0:
                newtxts.append(t)
        txts = newtxts

    if wordtokenize:
        txtwords = [word_tokenize(t) for t in txts]
    else:
        txtwords = [string.split(t) for t in txts]
    txts = None

    if lowercase:
        txtwords = [[string.lower(w) for w in t] for t in txtwords]

    if removestopwords:
#        stoplist = stopwords.words("english")
        alphare = re.compile("[A-Za-z]")
        txtwords = [[w for w in t if w not in stoplist and alphare.search(w)] for t in txtwords]

    if stem:
        stemmer = PorterStemmer()
        txtwords = [[stemmer.stem(w) for w in t] for t in txtwords]

    txts = [string.join(words) for words in txtwords]

    return string.join(txts, sep="\n")

if __name__ == "__main__":
    import sys
    print textpreprocess(sys.stdin.read())
