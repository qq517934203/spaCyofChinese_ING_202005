
# coding: utf-8
"""Load vectors for a language trained using fastText
https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md
Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals
import plac
import numpy
import gensim
from gensim.models import Word2Vec
from gensim.models import Doc2Vec
from gensim.models import KeyedVectors
from gensim.models.word2vec import PathLineSentences
import spacy
from spacy.language import Language


@plac.annotations(
    vectors_loc=("Path to .vec file", "positional", None, str),
    lang=("Optional language ID. If not set, blank Language() will be used.",
          "positional", None, str))
def main(vectors_loc, lang=None):
    if lang is None:
        nlp = Language()
    else:
        # create empty language class – this is required if you're planning to
        # save the model to disk and load it back later (models always need a
        # "lang" setting). Use 'xx' for blank multi-language class.
        nlp = spacy.blank(lang)
    print('='*20)
    new_model = KeyedVectors.load_word2vec_format(vectors_loc,binary=True)
    for word in new_model.wv.index2word: 
        vector = numpy.asarray([float(v) for v in new_model[word]], dtype='f')
        nlp.vocab.set_vector(word, vector)  # add the vectors to the vocab
        # print(word, vector)
    print('='*20)
 
    # test the vectors and similarity
    # text = '不同'
    # doc = nlp(text)
    # print(text, doc[0].similarity(doc[1]))
    # print('='*20)
    nlp.to_disk("./zh_model")


if __name__ == '__main__':
    plac.call(main)