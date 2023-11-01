import json
import asyncio
from downloaders.tiktok_downloader import TikTokVideoDownloader
from scrapers.tiktok_video_metadata_scraper import TiktokVideoMetadataScraper
from transcribers.tiktok_video_to_text import SpeechConverter
from nlp.sentiment_analysis import SentimentAnalyzer
from cv.face_detection import FaceDetection

def main():
    print(
        '''


   __     __ __         __              __         
  |  \   |  \  \       |  \            |  \        
 _| ▓▓_   \▓▓ ▓▓   __ _| ▓▓_    ______ | ▓▓   __   
|   ▓▓ \ |  \ ▓▓  /  \   ▓▓ \  /      \| ▓▓  /  \  
 \▓▓▓▓▓▓ | ▓▓ ▓▓_/  ▓▓\▓▓▓▓▓▓ |  ▓▓▓▓▓▓\ ▓▓_/  ▓▓  
  | ▓▓ __| ▓▓ ▓▓   ▓▓  | ▓▓ __| ▓▓  | ▓▓ ▓▓   ▓▓   
  | ▓▓|  \ ▓▓ ▓▓▓▓▓▓\  | ▓▓|  \ ▓▓__/ ▓▓ ▓▓▓▓▓▓\   
   \▓▓  ▓▓ ▓▓ ▓▓  \▓▓\  \▓▓  ▓▓\▓▓    ▓▓ ▓▓  \▓▓\  
    \▓▓▓▓ \▓▓\▓▓   \▓▓   \▓▓▓▓  \▓▓▓▓▓▓ \▓▓   \▓▓  
                                                   
     __              __ __                   
    |  \            |  \  \                  
   _| ▓▓_    ______ | ▓▓ ▓▓ ______   ______  
  |   ▓▓ \  /      \| ▓▓ ▓▓/      \ /      \ 
   \▓▓▓▓▓▓ |  ▓▓▓▓▓▓\ ▓▓ ▓▓  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\ 
    | ▓▓ __| ▓▓    ▓▓ ▓▓ ▓▓ ▓▓    ▓▓ ▓▓   \▓▓  
    | ▓▓|  \ ▓▓▓▓▓▓▓▓ ▓▓ ▓▓ ▓▓▓▓▓▓▓▓ ▓▓      
     \▓▓  ▓▓\▓▓     \ ▓▓ ▓▓\▓▓     \ ▓▓      
      \▓▓▓▓  \▓▓▓▓▓▓▓\▓▓\▓▓ \▓▓▓▓▓▓▓\▓▓      
    '''
    )
    
    print(
        '''
╔══════════════════════════════════════════════╗
║                                              ║
║    Choose from the options below:            ║
║                                              ║
║     [1] ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴛɪᴋᴛᴏᴋ ᴠɪᴅᴇᴏ (ᴜʀʟ)        ║
║     [2] ᴛʀᴀɴsᴄʀɪʙᴇ ᴀ ᴛɪᴋᴛᴏᴋ ᴠɪᴅᴇᴏ (ᴍᴘ4)      ║
║     [3] ᴀɴᴀʟʏᴢᴇ ᴀ ᴛɪᴋᴛᴏᴋ ᴠɪᴅᴇᴏ (ᴍᴘ4/ᴊsᴏɴ)    ║
║     [exit] ᴏ̨ᴜɪᴛ ᴛʜᴇ ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ              ║
║                                              ║
╚══════════════════════════════════════════════╝
        '''
    )
    
    while True:
        # Prompt the user for input
        user_input = input("Enter a command (1, 2, 3, or 'exit' to quit): ")

        # Check the user's input and perform tasks accordingly
        if user_input == '1':
            print("\nYou selected option 1: 'Download a Tiktok Video.'\n")
            url = input("Enter tiktok video URL: ")
            scraper = TiktokVideoMetadataScraper(str(url))
            asyncio.get_event_loop().run_until_complete(scraper.scrape_data_and_save_to_json())
            downloader = TikTokVideoDownloader([str(url)])
            downloader.download_tiktok_videos(browser='pyppeteer')

        elif user_input == '2':
            print("\nYou selected option 2: 'Transcribe a Tiktok Video.'\n")
            mp4 = input("Enter mp4 filepath: ")
            speech_converter = SpeechConverter(f'{mp4}')
            speech_converter.extract_and_transform_speech()

        elif user_input == '3':
            print("\nYou selected option 3: 'Analyze a Tiktok Video.'\n")
            face_detection = input("Do you want face detection? (y/n): ")
            nlp = input("Do you want NLP? (y/n): ")
            if face_detection in ['y', 'yes', 'Y', 'YES', 'Yes']:
                print('\nRad...\n')
                mp4 = input("Enter mp4 filepath: ")
                detector = FaceDetection(mp4)
                detector.detect_faces()
            else:
                pass
            if nlp in ['y', 'yes', 'Y', 'YES', 'Yes']:
                print('\nCool...\n')
                filepath = input("Enter your data filepath: ")
                if filepath.endswith('.mp4'):
                    speech_converter = SpeechConverter(f'{filepath}')
                    text = speech_converter.extract_and_transform_speech()
                elif filepath.endswith('.json'): 
                    with open(f'{filepath}', 'r') as file:
                        data = json.load(file)
                    text = data['text']['text']
                analyzer = SentimentAnalyzer()
                analyzer.analyze_comments(text, filepath)
            else:
                pass                

        elif user_input.lower() == 'exit':
            print("\nExiting the program. Goodbye!\n")
            break 
        
        else:
            print("\n")

if __name__ == "__main__":
    main()