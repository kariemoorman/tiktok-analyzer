import spacy
import json
import pandas as pd

nlp = spacy.load("en_core_web_md")


        
def extract_keywords(document):

    doc = nlp(document)
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha and not token.is_punct]
    lemmas = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha and not token.is_punct]
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    adjs = [token.text for token in doc if token.pos_ == "ADJ"]
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

    return tokens, lemmas, nouns, verbs, adjs, noun_phrases, prep_phrases, verb_phrases
