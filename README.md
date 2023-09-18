## TikTok-Teller
#### Description: TikTok Video Scraping and Content Analysis Tool.

---
### Repository Contents
- <b>TikTok Video Scrapers</b>
  - [tiktok_user_video_scraper.py](https://github.com/kariemoorman/tiktok-teller/blob/main/tiktok/__scripts/tiktok_scraper/tiktok_user_video_scraper.py)  
    Choose either Selenium or Pyppeteer to dynamically scrape TikTok videos for one or more Tiktok usernames.  
      E.g., ```python3 tiktok_user_video_scraper.py blitzphd eczachly -b pyppeteer -o csv```

  - [tiktok_tag_video_scraper.py](https://github.com/kariemoorman/tiktok-teller/blob/main/tiktok/__scripts/tiktok_scraper/tiktok_tag_video_scraper.py)
    Choose either Selenium or Pyppeteer to dynamically scrape TikTok videos for one or more Tiktok tags.  
    E.g., ```python3 tiktok_tag_video_scraper.py physics lhc -b pyppeteer -o csv```

- <b>TikTok Video Downloader</b>
  - [tiktok_downloader.py](https://github.com/kariemoorman/tiktok-teller/blob/main/tiktok/__scripts/tiktok_downloader.py)  
    Choose either Selenium or Pyppeteer to dynamically download one or more Tiktok videos.  
      E.g., ```python3 tiktok_downloader.py <url> -b selenium -d firefox```

- <b>TikTok Video Speech to Text Extractor</b>
  - [tiktok_video_to_text.py](https://github.com/kariemoorman/tiktok-teller/blob/main/tiktok/__scripts/tiktok_video_to_text.py)  
    Choose either Google or OpenAI ASR model to transcribe Tiktok video (in mp4 format).  
      E.g., ```python3 tiktok_video_to_text.py <path/to/video_filename.mp4> -m openai```



---

<p align='center'><b>License: <a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU General 
Public License v3.0</a></b></p>

