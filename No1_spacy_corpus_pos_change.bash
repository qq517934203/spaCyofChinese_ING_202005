download file http://file.hankcs.com/corpus/chs-gsd-ud.zip
mkdir -p corpus/spacy

python -m spacy convert spacy_corpus_pos/UD_Chinese-GSD-master/chs_gsd-ud-train.conllu spacy_corpus_pos/spacy
python -m spacy convert spacy_corpus_pos/UD_Chinese-GSD-master/chs_gsd-ud-dev.conllu spacy_corpus_pos/spacy
python -m spacy convert spacy_corpus_pos/UD_Chinese-GSD-master/chs_gsd-ud-test.conllu spacy_corpus_pos/spacy
