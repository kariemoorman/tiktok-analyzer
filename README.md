<h2 align='center'>TikTok-Analyzer: A TikTok Video Scraping and Content Analysis Tool</h2>


<p align='center'><img src='https://github.com/kariemoorman/tiktok-analyzer/blob/main/tiktok-analyzer.png' alt="Tiktok-Teller" width='50%;' ></p>

### Description

Search & download Tiktok videos by username and/or video tag, and analyze video contents. Transcribe video speech to text and perform NLP analysis tasks (e.g., keyword and topic discovery; emotion/sentiment analysis). Isolate audio signal and perform signal processing analysis tasks (e.g., pitch, prosody and sentiment analysis). Isolate visual stream and perform image tasks (e.g., object detection; face detection).

---

### Python Toolkit
- Web Scraping: [Pyppeteer](https://pyppeteer.github.io/pyppeteer/), [Selenium](https://www.selenium.dev/)
- Transcription: [OpenAI Whisper](https://openai.com/research/whisper)
- NLP: [SpaCy](https://spacy.io/), [NLTK](https://www.nltk.org/)
- CV: [OpenCV](https://opencv.org/)

---

### Installation & Use

<details>
<summary><b>Virtual Env</b></summary>
<br>

- Clone or download .zip of `tiktok-analyzer` python package.
```
git clone https://github.com/kariemoorman/tiktok-analyzer.git
```

- Create a virtual environment inside the `tiktok-analyzer` directory.
```
cd tiktok-analyzer && python3 -m venv .venv 
```

- Activate virtual environment.  
```
source .venv/bin/activate
```

- Install package dependencies. 
```
pip install -r requirements.txt

- Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

- Install ffmpeg
brew install ffmpeg
```

- Execute `tiktok-analyzer` program.
```
python src/tiktok-analyzer.py
```
</details>

<details>
<summary><b>Docker Image</b></summary>
<br>

- Clone or download .zip of `tiktok-analyzer` python package.
```
git clone https://github.com/kariemoorman/tiktok-analyzer.git
```

- Build Docker image.
```
docker build -t tt-analyzer .
```

- Run Docker image as container.
```
docker run --rm -ti tt-analyzer
```
</details>

---

### Repository Contents
<details>
<summary><b>TikTok Video Scrapers</b></summary>
<br>
  
  - [tiktok_user_video_scraper.py](https://github.com/kariemoorman/tiktok-analyzer/blob/main/src/scrapers/tiktok_user_video_scraper.py)  
    Choose either Selenium or Pyppeteer to dynamically scrape TikTok videos for one or more Tiktok usernames.  
      E.g., ```python3 tiktok_user_video_scraper.py <username> <username> -b pyppeteer -o csv```

  - [tiktok_tag_video_scraper.py](https://github.com/kariemoorman/tiktok-analyzer/blob/main/src/scrapers/tiktok_tag_video_scraper.py)  
    Choose either Selenium or Pyppeteer to dynamically scrape TikTok videos for one or more Tiktok tags.  
    E.g., ```python3 tiktok_tag_video_scraper.py physics lhc -b pyppeteer -o csv```

  - [tiktok_video_metadata_scraper.py](https://github.com/kariemoorman/tiktok-analyzer/blob/main/src/scrapers/tiktok_video_metadata_scraper.py)  
    Export metadata from a Tiktok video.  
    E.g., ```python3 tiktok_video_metadata_scraper.py <tiktok_video_url>```

<br>
</details>

<details>
<summary><b>TikTok Video Downloaders</b></summary>
<br>

  - [tiktok_downloader.py](https://github.com/kariemoorman/tiktok-analyzer/blob/main/src/downloaders/tiktok_downloader.py)   
    Choose either Selenium or Pyppeteer to dynamically download one or more Tiktok videos.  
      E.g., ```python3 tiktok_downloader.py <tiktok_video_url> -b selenium -d firefox```

<br>
</details>

<details>
<summary><b>Speech Transcription</b></summary>
<br>
  
  - [tiktok_video_to_text.py](https://github.com/kariemoorman/tiktok-analyzer/blob/main/src/transcribers/tiktok_video_to_text.py)  
    Choose either Google or OpenAI ASR model to transcribe Tiktok video (in mp4 format).  
      E.g., ```python3 tiktok_video_to_text.py <path/to/video_filename.mp4> -m openai```

<br>
</details>

<details>
<summary><b>CV Object/Face Detection</b></summary>
<br>
  
  - [face_detection.py](https://github.com/kariemoorman/tiktok-analyzer/blob/main/src/cv/face_detection.py)  
    Conduct face detection task on Tiktok video (in mp4 format).  
      E.g., ```python3 face_detection.py <video.mp4> -o 'output/file/path'```

<br>
</details>

<details>
<summary><b>NLP Analysis</b></summary>
<br>
  
  - [sentiment_analysis.py](https://github.com/kariemoorman/tiktok-analyzer/blob/main/src/nlp/sentiment_analysis.py)  
    Conduct sentiment analysis tasks on Tiktok video transcription data.  
      E.g., ```python3 sentiment_analysis.py -t <document> -f 'output/file/path/filename.mp4/json'```

<br>
</details>

---

### Use Cases 

<details>
<summary><b>Option 1: Download a Tiktok Video.</b></summary>
<br>

- Input URL: https://www.tiktok.com/@bytesiz3/video/7290398845777825070
- Output: 
  - Metadata: [@bytesiz3_video_7290398845777825070_metadata.json](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/%40bytesiz3_video_7290398845777825070_metadata.json)
  - MP4: [ssstik.io_1698796057176.mp4](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.mp4)

<br>

</details>

<details>
<summary><b>Option 2: Transcribe a Tiktok Video.</b></summary>
<br>

- Input MP4: [ssstik.io_1698796057176.mp4](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.mp4)
- Output:
  - JSON: [ssstik.io_1698796057176.json](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.json)
  - CSV: [ssstik.io_1698796057176.csv](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.csv)
  - MP3: [ssstik.io_1698796057176.mp3](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.mp3)

<br>

</details>

<details>
<summary><b>Option 3: Analyze a Tiktok Video.</b></summary>
<br>
  
- Input MP4: [ssstik.io_1698796057176.mp4](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.mp4)
- Output: 
  - Face Detection: 
    - MP4: [ssstik.io_1698796057176.mp4.cv_output.mp4](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.mp4.cv_output.mp4)
    - Faces Directory: [ssstik.io_1698796057176_faces/](https://github.com/kariemoorman/tiktok-analyzer/tree/main/example_data/ssstik.io_1698796057176_faces)
  - NLP:
    - Sentiment analysis: [ssstik.io_1698796057176.sentiment_analysis.txt](https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.sentiment_analysis.txt)

<br>

</details>

---

### Example Use Case: Analyze Video (Face Detection & NLP)

<p align='left'><img src='https://github.com/kariemoorman/tiktok-analyzer/blob/main/example_data/ssstik.io_1698796057176.mp4-cv_output.gif' alt='example_gif' height='400'></p>

```
Text:  How you can check up a URL is safe. Go to Google and type transparency report. You can enter. Click this first one. We're going to go to Google safe browsing. Site status. And here you can enter the URL. Stay safe, follow for more.

Tokens: ['how', 'you', 'can', 'check', 'up', 'a', 'url', 'is', 'safe', 'go', 'to', 'google', 'and', 'type', 'transparency', 'report', 'you', 'can', 'enter', 'click', 'this', 'first', 'one', 'we', 'going', 'to', 'go', 'to', 'google', 'safe', 'browsing', 'site', 'status', 'and', 'here', 'you', 'can', 'enter', 'the', 'url', 'stay', 'safe', 'follow', 'for', 'more']

Lemmas: ['how', 'you', 'can', 'check', 'up', 'a', 'url', 'be', 'safe', 'go', 'to', 'google', 'and', 'type', 'transparency', 'report', 'you', 'can', 'enter', 'click', 'this', 'first', 'one', 'we', 'go', 'to', 'go', 'to', 'google', 'safe', 'browsing', 'site', 'status', 'and', 'here', 'you', 'can', 'enter', 'the', 'url', 'stay', 'safe', 'follow', 'for', 'more']

Determiners (Dets): ['a', 'this', 'the']

Nouns: ['url', 'type', 'transparency', 'report', 'browsing', 'site', 'status', 'url']

Verbs: ['check', 'go', 'enter', 'click', 'go', 'go', 'google', 'enter', 'stay', 'follow']

Adjectives (Adjs): ['safe', 'first', 'safe', 'safe', 'more']

Adverbs (Advs): ['here']

Noun Phrases: ['you', 'a url', 'google and type transparency report', 'you', 'we', 'safe browsing', 'site status', 'you', 'the url']

Prepositional Phrases: ['to go', 'for follow']

Verb Phrases: ['check', 'go', 'enter', 'click', 'going go google', 'go google', 'google', 'here enter', 'stay follow', 'follow']

Emotion: Words: ['safe', 'safe', 'safe']

Sentence:  How you can check up a URL is safe.
Sentiment Score: 0.4404
Has Emotion: True
Is Derogatory: False
Derogatory Score: 0.00
Polarity: 0.5
Subjectivity: 0.5
Emotion_words: [(['safe'], 0.5, 0.5, None)]
------------------------------

Sentence: Go to Google and type transparency report.
Sentiment Score: 0.0
Has Emotion: False
Is Derogatory: False
Derogatory Score: 0.00
Polarity: 0.0
Subjectivity: 0.0
Emotion_words: []
------------------------------

Sentence: You can enter.
Sentiment Score: 0.0
Has Emotion: False
Is Derogatory: False
Derogatory Score: 0.00
Polarity: 0.0
Subjectivity: 0.0
Emotion_words: []
------------------------------

Sentence: Click this first one.
Sentiment Score: 0.0
Has Emotion: False
Is Derogatory: False
Derogatory Score: 0.00
Polarity: 0.25
Subjectivity: 0.3333333333333333
Emotion_words: [(['first'], 0.25, 0.3333333333333333, None)]
------------------------------

Sentence: We're going to go to Google safe browsing.
Sentiment Score: 0.4404
Has Emotion: True
Is Derogatory: False
Derogatory Score: 0.00
Polarity: 0.5
Subjectivity: 0.5
Emotion_words: [(['safe'], 0.5, 0.5, None)]
------------------------------

Sentence: Site status.
Sentiment Score: 0.0
Has Emotion: False
Is Derogatory: False
Derogatory Score: 0.00
Polarity: 0.0
Subjectivity: 0.0
Emotion_words: []
------------------------------

Sentence: And here you can enter the URL.
Sentiment Score: 0.0
Has Emotion: False
Is Derogatory: False
Derogatory Score: 0.00
Polarity: 0.0
Subjectivity: 0.0
Emotion_words: []
------------------------------

Sentence: Stay safe, follow for more.
Sentiment Score: 0.4404
Has Emotion: True
Is Derogatory: False
Derogatory Score: 0.00
Polarity: 0.5
Subjectivity: 0.5
Emotion_words: [(['safe'], 0.5, 0.5, None), (['more'], 0.5, 0.5, None)]
------------------------------
```

---

<p align='center'><b>License: <a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU General 
Public License v3.0</a></b></p>

