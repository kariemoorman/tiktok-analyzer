import sys
sys.path.append('/Users/karie/Github/tiktok-teller')

import unittest
from src.nlp.emotion_extractor import filter_words

class TestFilterWords(unittest.TestCase):
    def test_filter_words(self):
        test_text = "I am feeling happy and excited, but also a bit nervous."
        expected_emotion_words = ["happy", "excited", "nervous"]
        self.assertEqual(filter_words(test_text), expected_emotion_words)

    def test_empty_text(self):
        test_text = ""
        expected_emotion_words = []
        self.assertEqual(filter_words(test_text), expected_emotion_words)

    def test_no_emotion_words(self):
        test_text = "This is a test sentence."
        expected_emotion_words = []
        self.assertEqual(filter_words(test_text), expected_emotion_words)

    def test_case_insensitivity(self):
        test_text = "I feel delighted and ecstatic!"
        expected_emotion_words = ["delighted", "ecstatic"]
        self.assertEqual(filter_words(test_text), expected_emotion_words)

if __name__ == '__main__':
    unittest.main()
