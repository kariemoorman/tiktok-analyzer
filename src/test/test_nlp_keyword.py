import sys
sys.path.append('/Users/karie/Github/tiktok-teller')

import unittest
from src.nlp.keyword_extractor import extract_keywords

class TestExtractKeywords(unittest.TestCase):
    def test_extract_keywords(self):
        test_document = "I'm testing this cool code from my head. It's extracting keywords effectively."
        tokens, lemmas, dets, nouns, verbs, adjs, advs, noun_phrases, prep_phrases, verb_phrases = extract_keywords(test_document)
        
        self.assertEqual(tokens, ['i', 'testing', 'this', 'cool', 'code', 'from', 'my', 'head', 'it', 'is', 'extracting', 'keywords', 'effectively'])
        self.assertEqual(lemmas, ['I', 'test', 'this', 'cool', 'code', 'from', 'my', 'head', 'it', 'be', 'extract', 'keyword', 'effectively'])
        self.assertEqual(dets, ['this'])
        self.assertEqual(nouns, ['code', 'head', 'keywords',])
        self.assertEqual(verbs, ['test', 'extract'])
        self.assertEqual(adjs, ['cool'])
        self.assertEqual(advs, ['effectively'])
        self.assertEqual(noun_phrases, ['i', 'this cool code', 'my head', 'it', 'keywords'])
        self.assertEqual(prep_phrases, ['from testing' ]) #, 'from my head'])
        self.assertEqual(verb_phrases, ['testing', 'extracting effectively'])

    def test_empty_document(self):
        test_document = ""
        tokens, lemmas, dets, nouns, verbs, adjs, advs, noun_phrases, prep_phrases, verb_phrases = extract_keywords(test_document)

        self.assertEqual(tokens, [])
        self.assertEqual(lemmas, [])
        self.assertEqual(dets, [])
        self.assertEqual(nouns, [])
        self.assertEqual(verbs, [])
        self.assertEqual(adjs, [])
        self.assertEqual(advs, [])
        self.assertEqual(noun_phrases, [])
        self.assertEqual(prep_phrases, [])
        self.assertEqual(verb_phrases, [])

if __name__ == '__main__':
    unittest.main()
