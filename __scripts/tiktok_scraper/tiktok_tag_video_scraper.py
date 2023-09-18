#!/usr/bin/python

import os
import time
import asyncio
import argparse
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from pyppeteer import launch


class TikTokScraper:
    ''' 
    Function:
    For each tag in tag list, extract video title and video URL.
    Write results as CSV, JSON, or PARQUET.
    
    Input Values:
    Tag: Input type list of (str) tiktok tags (without #). 
    Browser: Input type (str), either "selenium" or "pyppeteer." Default = 'pyppeteer'.
    File Format: Input type (str), either "csv", "json" or "parquet." Default = 'csv'.
    
    Example: 
    python3 tiktok_tag_video_scraper.py amazonscam --b pyppeteer --o csv
    '''
    
    def __init__(self, browser, output_file_format):
        self.snapshotdate = datetime.today().strftime('%d-%b-%Y')
        self.snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')
        self.tiktok_df = pd.DataFrame()
        self.browser = browser
        self.output_file_format = output_file_format
        print(f'Initiating task using {browser}...')

    async def _scroll_to_end_selenium(self, driver):
        SCROLL_PAUSE_TIME = 30
        # Get the height of the whole page
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            # Check for end of the page
            if new_height == last_height:
                break
            # Update the scroll height for the next iteration
            last_height = new_height
        time.sleep(10)

    async def _scroll_to_end_pyppeteer(self, page):
        SCROLL_PAUSE_TIME = 30
        # Get the height of the whole page
        last_height = await page.evaluate('() => document.body.scrollHeight')
        while True:
            # Scroll to the bottom of the page
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight);')
            await asyncio.sleep(SCROLL_PAUSE_TIME)
            # Check for end of the page
            new_height = await page.evaluate('() => document.body.scrollHeight')
            if new_height == last_height:
                break
            # Update the scroll height for the next iteration
            last_height = new_height

    async def _extract_data_selenium(self, tag, driver):
        url = f"https://www.tiktok.com/tag/{tag}"
        driver.get(url)
        await self._scroll_to_end_selenium(driver)
        # Extract video titles and urls
        div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.DivItemContainerV2')
        titles = []
        hrefs = []
        tags = []
        for div_element in div_elements:
            a_element = div_element.find_element(By.TAG_NAME, 'a')
            title = a_element.get_attribute('title')
            href = a_element.get_attribute('href')
            titles.append(title)
            hrefs.append(href)
            tags.append(tag)
            
        os.makedirs(f"../__data/__tiktoks/{tag}", exist_ok=True)
        self.tiktok_df['tag'] = tags
        self.tiktok_df['url'] = hrefs
        self.tiktok_df['title'] = titles
        self._save_to_file(tag)

    async def _extract_data_pyppeteer(self, page, tag):
        url = f"https://www.tiktok.com/tag/{tag}"
        await page.goto(url)
        await self._scroll_to_end_pyppeteer(page)
        # Extract video titles and urls
        div_elements = await page.querySelectorAll('div.DivItemContainerV2')
        titles = []
        hrefs = []
        tags = []
        for div_element in div_elements:
            a_element = await div_element.querySelector('a')
            title = await a_element.evaluate('(element) => element.getAttribute("title")')
            href = await a_element.evaluate('(element) => element.getAttribute("href")')
            titles.append(title)
            hrefs.append(href)
            tags.append(tag)

        os.makedirs(f"../__data/__tiktoks/{tag}", exist_ok=True)
        self.tiktok_df['tag'] = tags
        self.tiktok_df['url'] = hrefs
        self.tiktok_df['title'] = titles
        self._save_to_file(tag)

    def _save_to_file(self, tag):
        if self.output_file_format == 'json':
            self.tiktok_df.to_json(f"../__data/__tiktoks/{tag}/{tag}__tiktok_videos_{self.snapshotdatetime}.json", orient='records')
        elif self.output_file_format == 'parquet':
            self.tiktok_df.to_parquet(f"../__data/__tiktoks/{tag}/{tag}__tiktok_videos_{self.snapshotdatetime}.parquet", index=False, compression='gzip')
        elif self.output_file_format == 'csv':
            self.tiktok_df.to_csv(f"../__data/__tiktoks/{tag}/{tag}__tiktok_videos_{self.snapshotdatetime}.csv", index=False, sep='\t', encoding='utf-8')
    
    async def scrape_tag_video(self, tag_list):
        if self.browser == 'selenium':
            CHROMEDRIVER_PATH = ""
            CHROME_PATH = ""
            WINDOW_SIZE = "1920,1080"
            options = ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--window-size=%s" % WINDOW_SIZE)
            options.binary_location = CHROME_PATH
            prefs = {'profile.managed_default_content_settings.images': 2}
            options.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(options=options)
            for tag in tag_list:
                await self._extract_data_selenium(tag, driver)
            driver.quit()

        elif self.browser == 'pyppeteer':
            browser = await launch(headless=True)
            page = await browser.newPage()
            for tag in tag_list:
                await self._extract_data_pyppeteer(page, tag)
            await browser.close()
        
        print("Task Complete!")


def main():
    parser = argparse.ArgumentParser(description="Scrape TikTok videos by tag.")
    parser.add_argument("tags", type=str, nargs="+", help="List of TikTok tags to scrape.")
    parser.add_argument("--browser","-b", type=str, choices=["selenium", "pyppeteer"], default="pyppeteer", help="Choose browser for scraping.")
    parser.add_argument("--output_file_format", "-o", type=str, choices=["csv", "json", "parquet"], default="csv", help="Choose output file format.")
    args = parser.parse_args()

    scraper = TikTokScraper(args.browser, args.output_file_format)
    asyncio.get_event_loop().run_until_complete(scraper.scrape_tag_video(args.tags))


if __name__ == "__main__":
    main()
