#!/usr/bin/python

import common.html2text
import common.tokenizer

#from nltk import word_tokenize
from nltk.tokenize import WordPunctTokenizer    # This is better for sentences containing unicode, like: u"N\u00faria Espert"
word_tokenize = WordPunctTokenizer().tokenize
from nltk.stem.porter import PorterStemmer
#from nltk.corpus import stopwords

import os.path
import re
import string

STOPFILE = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "english.stop")
stoplist = None

_wsre = re.compile("\s+")

def textpreprocess(txt, converthtml=True, sentencetokenize=True, removeblanklines=True, replacehyphenbyspace=True, wordtokenize=True, lowercase=True, removestopwords=True, stem=True, removenonalphanumericchars=True, stemlastword=False, stripallwhitespace=False):
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

    if removeblanklines:
        newtxts = []
        for t in txts:
            if len(string.strip(t)) > 0:
                newtxts.append(t)
        txts = newtxts

    if replacehyphenbyspace:
        txts = [t.replace("-", " ") for t in txts]

    if wordtokenize:
        txtwords = [word_tokenize(t) for t in txts]
    else:
        txtwords = [string.split(t) for t in txts]
    txts = None

    if lowercase:
        txtwords = [[string.lower(w) for w in t] for t in txtwords]

    if removestopwords:
        txtwords = _removestopwords(txtwords)

    if stem:
        txtwords = _stem(txtwords)

    # TODO: Maybe remove Unicode accents? http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string

    if removenonalphanumericchars:
        txtwords = _removenonalphanumericchars(txtwords)

    txtwords = [[w for w in t if w != ""] for t in txtwords]

    if stemlastword:
        txtwords = _stemlastword(txtwords)

    txts = [string.join(words) for words in txtwords]

    if stripallwhitespace:
        txts = _stripallwhitespace(txts)

    return string.join(txts, sep="\n")

def _removestopwords(txtwords):
    global stoplist
#    stoplist = stopwords.words("english")
    if stoplist is None:
        stoplist = frozenset([string.strip(l) for l in open(STOPFILE).readlines()])
    return [[w for w in t if w not in stoplist] for t in txtwords]

def _stem(txtwords):
    stemmer = PorterStemmer()
    return [[stemmer.stem(w) for w in t] for t in txtwords]

def _removenonalphanumericchars(txtwords):
    alphanumre = re.compile("[\w\-\' ]", re.UNICODE)
    return [[string.join([c for c in w if alphanumre.search(c) is not None], "") for w in t] for t in txtwords]

def _stemlastword(txtwords):
    stemmer = PorterStemmer()
    return [t[:-1] + [stemmer.stem(t[-1])] for t in txtwords if len(t) > 0]

def _stripallwhitespace(txts):
    return [_wsre.sub("", txt) for txt in txts]

if __name__ == "__main__":
    import sys
    print textpreprocess(sys.stdin.read())
