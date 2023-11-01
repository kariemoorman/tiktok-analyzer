## TikTok-Teller
#### Description: TikTok Video Scraping and Content Analysis Tool

<img src='https://github.com/kariemoorman/tiktok-teller/blob/main/tiktok-teller.png'>

Search & download Tiktok videos by username and/or video tag, and analyze video contents. Transcribe video speech to text and perform NLP analysis tasks (e.g., keyword and topic discovery; emotion/sentiment analysis). Isolate audio signal and perform signal processing analysis tasks (e.g., pitch, prosody and sentiment analysis). Isolate visual stream and perform image tasks (e.g., object detection; face detection).

---
### Repository Contents
- <b>TikTok Video Scrapers</b>
  - [tiktok_user_video_scraper.py](https://github.com/kariemoorman/tiktok-teller/blob/main/src/scrapers/tiktok_user_video_scraper.py)  
    Choose either Selenium or Pyppeteer to dynamically scrape TikTok videos for one or more Tiktok usernames.  
      E.g., ```python3 tiktok_user_video_scraper.py blitzphd eczachly -b pyppeteer -o csv```

  - [tiktok_tag_video_scraper.py](https://github.com/kariemoorman/tiktok-teller/blob/main/src/scrapers/tiktok_tag_video_scraper.py)
    Choose either Selenium or Pyppeteer to dynamically scrape TikTok videos for one or more Tiktok tags.  
    E.g., ```python3 tiktok_tag_video_scraper.py physics lhc -b pyppeteer -o csv```

  - [tiktok_video_metadata_scraper.py](https://github.com/kariemoorman/tiktok-teller/blob/main/src/scrapers/tiktok_video_metadata_scraper.py)
    Export metadata from a Tiktok video.  
    E.g., ```python3 tiktok_video_metadata_scraper.py <url>```
    

- <b>TikTok Video Downloader</b>
  - [tiktok_downloader.py](https://github.com/kariemoorman/tiktok-teller/blob/main/src/downloaders/tiktok_downloader.py) 
    Choose either Selenium or Pyppeteer to dynamically download one or more Tiktok videos.  
      E.g., ```python3 tiktok_downloader.py <url> -b selenium -d firefox```

- <b>TikTok Video Speech Transcriber</b>
  - [tiktok_video_to_text.py](https://github.com/kariemoorman/tiktok-teller/blob/main/src/transcribers/tiktok_video_to_text.py)  
    Choose either Google or OpenAI ASR model to transcribe Tiktok video (in mp4 format).  
      E.g., ```python3 tiktok_video_to_text.py <path/to/video_filename.mp4> -m openai```

- <b>TikTok Video Face Detection</b>
  - [face_detection.py](https://github.com/kariemoorman/tiktok-teller/blob/main/src/cv/face_detection.py)  
    Conduct face detection task on Tiktok video (in mp4 format).  
      E.g., ```python3 face_detection.py <video.mp4> -o 'output/file/path'```

- <b>TikTok Sentiment Analysis</b>
  - [sentiment_analysis.py](https://github.com/kariemoorman/tiktok-teller/blob/main/src/nlp/sentiment_analysis.py)  
    Conduct sentiment analysis tasks on Tiktok video transcription data.  
      E.g., ```python3 sentiment_analysis.py -t <document> -f 'output/file/path'```
    

---

<p align='center'><b>License: <a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU General 
Public License v3.0</a></b></p>

