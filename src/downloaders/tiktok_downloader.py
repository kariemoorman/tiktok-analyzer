import re
import time
import asyncio
import argparse
import keyboard
import random
from pyppeteer import launch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By


class TikTokVideoDownloader:
    def __init__(self, url_list):
        self.url_list = url_list
        self.comment_scraper_url = 'https://ssstik.io/en'
        # Set user agent
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        # Add random delay for time.sleep functions
        self.min_delay = 5
        self.max_delay = 15
        self.random_delay = random.uniform(self.min_delay, self.max_delay)
    
    def download_videos_pyppeteer(self):
        asyncio.get_event_loop().run_until_complete(self._pyppeteer_tiktok_video_downloader())

    async def _pyppeteer_tiktok_video_downloader(self):
        # Set up the browser using pyppeteer
        browser = await launch(args=['--no-sandbox'])
        page = await browser.newPage()
        
        # Set the User-Agent header
        await page.setUserAgent(self.user_agent)
        
        # Content injection and button locations
        url_location = '//input[@id="main_page_text"]'
        submit_button_location = '//button[@class="pure-button-primary"]'
        download_button_location = '//a[@class="pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark vignette_active notranslate"]'

        for url in self.url_list:
            # Extract video identification
            username_video_id = re.sub("https://www.tiktok.com/@", "", url)
            username_videoid_noslash = re.sub(r"\/", "_", username_video_id)
            print("Downloading tiktok video:", username_videoid_noslash)

            await page.goto(self.comment_scraper_url)
            await asyncio.sleep(self.random_delay)

            # Paste URL
            url_input = await page.waitForXPath(url_location)
            await url_input.type(url)

            # Click submit button
            submit_button = await page.waitForXPath(submit_button_location)
            await submit_button.click()

            # Wait for the download button to appear and click it
            await asyncio.sleep(12)
            download_button = await page.waitForXPath(download_button_location)
            await download_button.click()
            keyboard.press_and_release("command+left")
            
            await asyncio.sleep(self.random_delay)
            print('TikTok Video Download Complete!')

        await browser.close()
    
    def download_videos_selenium(self, driver):
        #comment_scraper_url = 'https://ssstik.io/en'
        # Specify Selenium Driver
        
        
        if driver == 'chrome':
            CHROMEDRIVER_PATH = ""
            CHROME_PATH = ""
            WINDOW_SIZE = "1920,1080"
            options = ChromeOptions()
            options.add_argument(f"user-agent={self.user_agent}")
            options.add_argument("--headless")  
            options.add_argument("--no-sandbox")  
            options.add_argument("--window-size=%s" % WINDOW_SIZE)
            options.binary_location = CHROME_PATH
            prefs = {'profile.managed_default_content_settings.images':2}
            options.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(options=options)

        if driver == 'firefox':
            FIREFOXDRIVER_PATH = ""
            FIREFOX_PATH = ""
            WINDOW_SIZE = "1920,1080"
            options = FirefoxOptions()
            options.add_argument(f"user-agent={self.user_agent}")
            #options.add_argument("--headless")  
            options.add_argument("--window-size=%s" % WINDOW_SIZE)

            driver = webdriver.Firefox(options=options)

        url_location = '//input[@id="main_page_text"]'
        submit_button_location = '//button[@class="pure-button-primary"]'
        download_button_location = '//a[@class="pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark vignette_active notranslate"]'
        
        for url in self.url_list: 
            # Extract video identification 
            username_video_id = re.sub("https://www.tiktok.com/@","", url)
            username_videoid_noslash = re.sub(r"\/","_", username_video_id)
            print(username_videoid_noslash)
            # Open URL
            driver.get(self.comment_scraper_url)
            time.sleep(self.random_delay)
            #paste URL 
            driver.find_element(By.XPATH, url_location).send_keys(url)		
            #select submit button
            driver.find_element(By.XPATH, submit_button_location).click()
            time.sleep(12)
            #select download button
            driver.find_element(By.XPATH, download_button_location).click()
            time.sleep(self.random_delay)
            # keyboard.write(f"ssstik_{username_videoid_noslash}")
            # time.sleep(5)
            keyboard.press_and_release("command+left")
            #keyboard.press_and_release("enter")
            time.sleep(self.random_delay)
            driver.quit()

    def download_tiktok_videos(self, browser='selenium', driver='chrome'):
        if browser == 'pyppeteer':
            self.download_videos_pyppeteer()
        elif browser == 'selenium':
            self.download_videos_selenium(driver)


def main():
    parser = argparse.ArgumentParser(description="Download TikTok videos using ssstik.io")
    parser.add_argument("urls", nargs='+', help="List of TikTok video URLs to download")
    parser.add_argument("--browser","-b", type=str, choices=["pyppeteer", "selenium"], help="Browser to use for downloading (default: selenium)")
    parser.add_argument("--driver","-d", type=str, choices=["chrome", "firefox"], help="Web Driver for use with Selenium (default: chrome)")
    
    args = parser.parse_args()

    downloader = TikTokVideoDownloader(args.urls)
    downloader.download_tiktok_videos(args.browser, args.driver)


if __name__ == "__main__":
    main()