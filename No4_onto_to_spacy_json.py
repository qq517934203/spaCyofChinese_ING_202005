import json  # for tuple support
import plac
import os
import re
from spacy.util import minibatch, compounding
import spacy
 
from tqdm import tqdm
import random
model =r'E:\python_py\spacy\new_cn_model_2\spacy_models\zh_core_web_sm'
nlp = spacy.load(model)


def get_root_filename(onto_dir):
    name_files = []
    for dirpath, subdirs, files in os.walk(onto_dir):
        for fname in files:
            if bool(re.search(".json", fname)):
                fn = os.path.join(dirpath, fname)
                fn = re.sub(".json", "", fn)
                name_files.append(fn)
    return name_files


def split_sentence(text):
    text = text.strip().split("\n")[1:-1]
    return text


def split_doc(text):
    text_list = text.strip().split("</DOC>\s<DOC")
    ids = [re.findall('<DOC DOCNO="(.+?)">', t)[0] for t in text_list]
    text_list = [re.sub('<DOC DOCNO=".+?">', "", t).strip() for t in text_list]
    return ids, text_list


def clean_ent(ent):
    tag = re.findall('TYPE="(.+?)"', ent)[0]
    text = re.findall(">(.+)", ent)[0]
    text = re.sub("\$", "\$", text)
    return (text, tag)


def raw_text(text):
    """Remove entity tags"""
    text = re.sub("<ENAMEX .+?>", "", text)
    text = re.sub("</ENAMEX>", "", text)
    return text


def ent_position(ents, text):
    search_point = 0
    spacy_ents = []
    for ent in ents:
        remain_text = text[search_point:]
        ma = re.search(ent[0], remain_text)
        ent_tup = (ma.start() + search_point, ma.end() + search_point, ent[1])
        spacy_ents.append(ent_tup)

        # update search point to prevent same word in different entity,
        # it will cause bug which hard to debug
        search_point = search_point + ma.end()
    return spacy_ents


def text_to_spacy(markup):
    raw_ents = re.findall("<ENAMEX(.+?)</ENAMEX>", markup)
    ents = [clean_ent(raw_ent) for raw_ent in raw_ents]
    text = raw_text(markup)
    spacy_ents = ent_position(ents, text)
    final = (text, {"entities": spacy_ents})
    return final


def onf_to_raw(onf_file):
    """
    Take in a path to a .onf Ontonotes file. Return the raw text (as much as possible).
    The quotes are usually quite messed up, so this is not going to look like real input text.
    """
    with open(onf_file, "r") as f:
        onf = f.read()
    sentences = re.findall(
        "Plain sentence\:\n\-+?\n(.+?)Treebanked sentence", onf, re.DOTALL
    )
    sentences = [re.sub("\n+?\s*", " ", i).strip() for i in sentences]
    paragraph = " ".join(sentences)
    return paragraph


def name_to_sentences(ner_filename):
    """
    Take a .name file and return a sentence list of the kind described here:
    https://github.com/explosion/spacy/blob/master/examples/training/training-data.json
    """

    with open(ner_filename, "r",encoding='utf-8') as f:
        doc = f.read()
    
    sentences = []
    onto_sents = split_sentence(doc)
    for id,sent in enumerate(onto_sents):
        # offsets = text_to_spacy(sent)
        # doc = nlp(offsets[0])
        # tags = biluo_tags_from_offsets(doc, offsets[1]["entities"])
        
        f_line = eval(sent)
        label = f_line['label']
        text = f_line['text']
        entities = {}
        tokens = []
        for (k,v) in  label.items(): 
            for (k2,v2) in v.items():
                t = {k2:k}
                entities.update(t)
        test_doc = nlp(text)
        for n, i in enumerate(test_doc):
            if str(i) in entities :
                token = {
                    "head": 0,
                    "dep": "",
                    "tag": "",
                    "orth": str(i),
                    "ner": 'U-'+str(entities[str(i)]),
                    "id": n,
                }
                tokens.append(token) 
            # elif
            else:
                token = {
                    "head": 0,
                    "dep": "",
                    "tag": "",
                    "orth": str(i),
                    "ner": 'O',
                    "id": n,
                }
                tokens.append(token) 
        sentences.append({"id": id, "paragraphs": [{"raw": f_line['text'], "sentences":[{"tokens": tokens}] }]})
    return sentences


def dir_to_annotation(ner_filename):
    try:
        sentences = name_to_sentences(ner_filename)
    except Exception as e:
        print("Error formatting ", ner_filename, e)
    return sentences



@plac.annotations(
    train_file_1=("Directory of cluener_public", "option", "i", str),
    val_file_1=("Directory of cluener_public", "option", "d", str),
    train_file=("File to write training spaCy JSON out to", "option", "t", str),
    val_file=("File to write validation spaCy JSON out to", "option", "e", str),
    val_split=("Percentage to use for evaluation", "option", "v", float),
)
def main(train_file_1, val_file_1 , train_file, val_file, val_split=0.75):
    print("Reading and formatting annotations")
    train_sen = dir_to_annotation(train_file_1)
    dev_sen = dir_to_annotation(val_file_1)
    # random.shuffle(all_annotations)
    # cutpoint = round(val_split * len(all_annotations))
    # val = all_annotations[:cutpoint]
    # train = all_annotations[cutpoint:]

    print(
        "Saving {0} training examples and {1} validation examples".format(
            len(train_sen), len(dev_sen)
        )
    )
    with open(train_file, "w",encoding='utf-8') as f:
        json.dump(train_sen, f, ensure_ascii=False, indent=4)
    with open(val_file, "w",encoding='utf-8') as f:
        json.dump(dev_sen, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    train_file_1 = r'E:\python_py\spacy\new_cn_model_2\spacy_ner\cluener_public\train.json'
    val_file_1 = r'E:\python_py\spacy\new_cn_model_2\spacy_ner\cluener_public\dev.json'
    train_file = r'E:\python_py\spacy\new_cn_model_2\spacy_ner\spacy\train.json'
    val_file = r'E:\python_py\spacy\new_cn_model_2\spacy_ner\spacy\dev.json'
    main(train_file_1, val_file_1 , train_file, val_file)

    # name_to_sentences(train_file_1)
    # print(sen)