#!/usr/bin/python3

import re
import csv
import json
import time
import timeit
from tqdm import tqdm
import subprocess
import argparse
from pydub import AudioSegment
import whisper
import speech_recognition as sr

class SpeechConverter:
    def __init__(self, mp4, method='openai'): 
        self.mp4 = mp4
        self.method = method
        self.basefilepath = re.match(r'(.*)\.mp4$', self.mp4).group(1)
        # OpenAI model
        self.model = whisper.load_model("base")
        
    def convert_mp4_to_mp3(self):
        # Construct output filename with .wav extension
        mp3_file = f"{self.basefilepath}.mp3"
        # Command to transform mp4 to mp3
        ffmpeg_command = [ "ffmpeg", "-i", self.mp4, "-vn", "-acodec", "mp3", mp3_file ]
        # Execute ffmpeg to transform mp4 to mp3
        try:
            subprocess.run(ffmpeg_command, check=True)
            print("\nMP3 Conversion successful.\n")
            return mp3_file
        except subprocess.CalledProcessError as e:
            print("Error during conversion:", e)
            return None
        
    def convert_mp3_to_wav(self, mp3):
        # Construct output filename with .wav extension
        wav_file = f"{self.basefilepath}.wav"
        # Execute transform mp3 to wav
        try:
            audio = AudioSegment.from_file(mp3)
            audio.export(wav_file, format="wav")
            print("WAV Conversion successful.\n")
            return wav_file
        except subprocess.CalledProcessError as e:
            print("Error during conversion:", e)
            return None
        
    def convert_speech_to_text(self, audio_file):
        if self.method == 'google':
            # Transform mp3 to wav
            wav_file = self.convert_mp3_to_wav(audio_file)
            # Initialize the recognizer
            recognizer = sr.Recognizer()
            # Use the recognizer to recognize speech
            with sr.AudioFile(wav_file) as source:
                # Calculate the audio file duration for progress tracking
                audio_duration = source.DURATION
                audio_data = recognizer.record(source, duration=audio_duration)
                # Initialize tqdm to track progress
                # progress_bar = tqdm(total=100, desc="Converting speech to text", unit="%", dynamic_ncols=True)
                try:
                    # Perform speech recognition
                    text = recognizer.recognize_google(audio_data)
                    # progress_bar.update(audio_duration)
                    print("Text extraction successful.\n")
                    return text
                except sr.UnknownValueError:
                    print("Speech recognition could not understand the audio.")
                    # progress_bar.close()
                    return None
                except sr.RequestError as e:
                    print("Could not request results from Google Web Speech API; {0}".format(e))
                    #time.sleep(1)
                    # progress_bar.close()
                    #return recognizer.recognize_google(audio_data)
                    return None
        elif self.method == 'openai': 
            try:
                result = self.model.transcribe(audio_file)
                # print(result["text"])
                return result
            except Exception as e:
                print(f"An error occurred: {e}")
                return None


    def save_as_json(self, text, output_file):
        with open(output_file, 'w') as json_file:
            json.dump(text, json_file, indent=4)
        print(f"\nData saved as JSON: {output_file}.\n")

    def save_as_csv(self, text, output_file):
        with open(output_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Text'])
            for item in text:
                csv_writer.writerow([item])
        print(f"Data saved as CSV: {output_file}.\n")
    
    def extract_and_transform_speech(self): 
        # Transform mp4 to mp3
        mp3_file = self.convert_mp4_to_mp3()
        # Transform speech to text
        extracted_text = self.convert_speech_to_text(mp3_file)
        # Write text to JSON and CSV
        if extracted_text:
            # Save as JSON
            self.save_as_json({"text": extracted_text}, f"{self.basefilepath}.json")
            # Save as CSV
            self.save_as_csv([extracted_text], f"{self.basefilepath}.csv")
        
def main(): 
    parser = argparse.ArgumentParser(description="Tiktok Video Speech and Text Extraction.")
    parser.add_argument("mp4", type=str, help="Tiktok video mp4 filepath.")
    parser.add_argument("-m", "--method", type=str, choices=['google','openai'], default='openai', help="Transcription method")
    args = parser.parse_args()
    
    speech_converter = SpeechConverter(args.mp4, args.method)
    speech_converter.extract_and_transform_speech()
    
if __name__ == "__main__":
    main()
