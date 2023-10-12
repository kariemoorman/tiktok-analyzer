import re
import spacy
import json
import pandas as pd

nlp = spacy.load("en_core_web_md")

        
def extract_keywords(document):
    # Minor alterations using regex
    string = re.sub(r"(\bi\'m\b)", "i am", document)
    string = re.sub(r"(\bi\'ve\b)", "i have", string)
    string = re.sub(r"(\bisn\'t\b)", "is not", string)
    string = re.sub(r"(\bit\'s\b)", "it is", string)
    string = re.sub(r"(\bwe\'re\b)", "we are", string)
    string = re.sub(r"(\bdidn\'t\b)", "did not", string)
    string = re.sub(r"(\bcan\'t\b)", "cannot", string)
    string = re.sub(r"(\b(?<=[a-z])n't\b)", " not", string)
    string = re.sub(r"((?<=[a-z])\'d\b)", " would", string)
    string = re.sub(r"((?<=[a-z])\'s\b)", " is", string)
    # Encode document in spacy
    doc = nlp(string.lower())
    tokens = [token.text for token in doc if token.is_alpha and not token.is_punct] #(not token.is_stop or token.text == "not")
    lemmas = [token.lemma_ for token in doc if token.is_alpha and not token.is_punct] #not token.is_stop
    dets = [token.text for token in doc if token.pos_ == "DET"]
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    adjs = [token.text for token in doc if token.pos_ == "ADJ"]
    advs = [token.text for token in doc if token.pos_ == "ADV"]
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    prep_phrases = []
    verb_phrases = []
    for token in doc:
        if token.dep_ == "prep":
            prep_phrase = token.text
            noun_chunk = token.head.text
            prep_phrases.append(f"{prep_phrase} {noun_chunk}")

        if "VERB" in token.pos_:
            verb_phrase = []
            for child in token.subtree:
                if child.pos_ in ("ADV", "VERB"):
                    verb_phrase.append(child.text)
            verb_phrases.append(" ".join(verb_phrase))

    return tokens, lemmas, dets, nouns, verbs, adjs, advs, noun_phrases, prep_phrases, verb_phrases


