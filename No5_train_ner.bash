#!/bin/bash
 
python -m spacy train zh spacy_models/ner_model spacy_ner/spacy/train.json spacy_ner/spacy/dev.json --pipeline ner -v spacy_models/dependency_model/model-best -m zh_model/meta.json -n 5
