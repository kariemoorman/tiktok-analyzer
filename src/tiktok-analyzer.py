import json
import asyncio
from downloaders.tiktok_downloader import TikTokVideoDownloader
from scrapers.tiktok_video_metadata_scraper import TiktokVideoMetadataScraper
from transcribers.tiktok_video_to_text import SpeechConverter
from nlp.sentiment_analysis import SentimentAnalyzer
from cv.face_detection import FaceDetection
from cv.object_detection import ObjectDetection


def main():
    print(
        '''
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗   
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝   
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝    
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗    
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗   
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   

    █████╗ ███╗   ██╗ █████╗ ██╗     ██╗   ██╗███████╗███████╗██████╗ 
   ██╔══██╗████╗  ██║██╔══██╗██║     ╚██╗ ██╔╝╚══███╔╝██╔════╝██╔══██╗
   ███████║██╔██╗ ██║███████║██║      ╚████╔╝   ███╔╝ █████╗  ██████╔╝
   ██╔══██║██║╚██╗██║██╔══██║██║       ╚██╔╝   ███╔╝  ██╔══╝  ██╔══██╗
   ██║  ██║██║ ╚████║██║  ██║███████╗   ██║   ███████╗███████╗██║  ██║
   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
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
        user_input = input("\nEnter a command (1, 2, 3, or 'exit' to quit): ")

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
            print('\n Rad...\n')
            object_detection = input("Do you want object detection? (y/n): ")
            print('\n Awesome...\n')
            nlp = input("Do you want NLP? (y/n): ")
            print('\n Cool...\n')
            if face_detection in ['y', 'yes', 'Y', 'YES', 'Yes']:
                mp4 = input("Enter mp4 filepath: ")
                detector = FaceDetection(mp4)
                print("\n...Starting Face Detection task...")
                detector.detect_faces()
                print("   Face Detection task complete!\n")
            else:
                mp4 = None
            if object_detection in ['y', 'yes', 'Y', 'YES', 'Yes']:
                if mp4 is None:
                    filepath = input("Enter mp4 filepath: ")
                else:
                    filepath = mp4
                detector = ObjectDetection(f'{filepath}')
                print("\n...Starting Object Detection task...")
                detector.detect_objects()
                print("   Object Detection task complete!\n")
            else:
                pass
            if nlp in ['y', 'yes', 'Y', 'YES', 'Yes']:
                if mp4 is None:
                    filepath = input("Enter mp4 filepath: ")
                else:
                    filepath = mp4
                speech_converter = SpeechConverter(f'{filepath}')
                text = speech_converter.extract_and_transform_speech()
                analyzer = SentimentAnalyzer()
                print("\n...Starting NLP analysis task...")
                analyzer.analyze_comments(text, filepath)
                print("   NLP analysis task complete!\n")
            else:
                pass
            
        elif user_input.lower() in ['exit', 'q', 'quit']:
            print("\nExiting the program. Goodbye!\n")
            break
        
        else:
            print("\n[!] Invalid entry. Please try again.")

if __name__ == "__main__":
    main()