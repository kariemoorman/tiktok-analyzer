import sys
sys.path.append('/Users/karie/Github/tiktok-teller')

import os
import unittest
from unittest.mock import patch
from src.transcribers.tiktok_video_to_text import SpeechConverter

class TestSpeechConverter(unittest.TestCase):
    
    def delete_mp3_file(self, filepath):
        if os.path.exists(filepath):
            if filepath.lower().endswith(".mp3"):
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            else:
                print(f"Not an MP3 file.")
            if filepath.lower().endswith(".wav"):
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            else:
                print(f"Not a WAV file.")
            if filepath.lower().endswith(".json"):
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            else:
                print(f"Not an JSON file.")
            if filepath.lower().endswith(".csv"):
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            else:
                print(f"Not an CSV file.")
        else:
            print(f"Does not exist in the directory.")


    def setUp(self):
        self.mp4_file = "/Users/karie/Github/tiktok-teller/src/test_data/ssstik.amy_k_nelson.liability_amzn.io_1680482656012.mp4"
        self.speech_converter = SpeechConverter(self.mp4_file, method="openai")

    def test_convert_mp4_to_mp3(self):
        # You can use a test MP4 file and assert the expected output
        expected_mp3_file = "/Users/karie/Github/tiktok-teller/src/test_data/ssstik.amy_k_nelson.liability_amzn.io_1680482656012.mp3"
        mp3_file = self.speech_converter.convert_mp4_to_mp3()
        self.assertEqual(mp3_file, expected_mp3_file)
        self.delete_mp3_file(expected_mp3_file)
        

    def test_convert_mp3_to_wav(self):
        # You can use a test MP3 file and assert the expected output
        mp3_file = self.speech_converter.convert_mp4_to_mp3()
        expected_wav_file = "/Users/karie/Github/tiktok-teller/src/test_data/ssstik.amy_k_nelson.liability_amzn.io_1680482656012.wav"
        wav_file = self.speech_converter.convert_mp3_to_wav(mp3_file)
        self.assertEqual(wav_file, expected_wav_file)
        self.delete_mp3_file(expected_wav_file)

    def test_convert_speech_to_text(self):
        # Mock the AudioFile context manager and recognizer to simulate speech recognition
        audio_file = "/Users/karie/Github/tiktok-teller/src/test_data/global_warming.mp3"
        expected_output = " Global warming is the long-term rise in the average temperature of the Earth's climate system"
        recognizer = self.speech_converter.convert_speech_to_text(audio_file)
        #print(recognizer['text'])
        self.assertEqual(recognizer['text'], expected_output)

    def test_save_as_json(self):
        # Test saving data as JSON and assert the existence of the JSON file
        data = {"text": "Test Speech Text"}
        json_file = "/Users/karie/Github/tiktok-teller/src/test_data/test.json"
        self.speech_converter.save_as_json(data, json_file)
        self.assertTrue(os.path.exists(json_file))
        self.delete_mp3_file(json_file)

    def test_save_as_csv(self):
        # Test saving data as CSV and assert the existence of the CSV file
        data = ["Test Speech Text"]
        csv_file = "/Users/karie/Github/tiktok-teller/src/test_data/test.csv"
        self.speech_converter.save_as_csv(data, csv_file)
        self.assertTrue(os.path.exists(csv_file))
        self.delete_mp3_file(csv_file)

if __name__ == '__main__':
    unittest.main()
