#!/usr/bin/python3
import re
import os
import asyncio
import json
import argparse
from pyppeteer import launch

class TiktokVideoMetadataScraper:
    def __init__(self, url):
        self.url = url
        self.output_file = self.output_file()
        
    def output_file(self):
        pattern = r'https://www\.tiktok\.com/(@\w+)/video/(\d+)'
        match = re.search(pattern, self.url)
        downloads_dir = os.path.expanduser("~" + os.path.sep + "Downloads/")
        if match:
            transformed_string = f"{match.group(1)}_video_{match.group(2)}"
        return downloads_dir + transformed_string + "_metadata.json"
            

    async def scroll_to_end_pyppeteer(self, page):
        SCROLL_PAUSE_TIME = 50
        last_height = await page.evaluate('() => document.body.scrollHeight')
        while True:
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight);')
            await asyncio.sleep(SCROLL_PAUSE_TIME)
            new_height = await page.evaluate('() => document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

    async def scrape_data_and_save_to_json(self):
        browser = await launch(headless=True)
        page = await browser.newPage()
        print('\nScraping video metadata...')
        try:
            await page.goto(self.url)
            await self.scroll_to_end_pyppeteer(page)

            title = await page.title()
            tags = await page.querySelectorAllEval('a[href*="tag"]', 'nodes => nodes.map(node => node.href)')
            channels = await page.querySelectorAllEval('a[href*="channel"]', 'nodes => nodes.map(node => node.href)')
            music = await page.querySelectorAllEval('a[href*="music"]', 'nodes => nodes.map(node => node.href)')
            place = await page.querySelectorAllEval('a[href*="place"]', 'nodes => nodes.map(node => node.href)')
            content = await page.content()
            #pattern = r'(\d+\.\d+[Kk]? Likes, \d+ Comments)'
            pattern = r'(?<=content=")(\d+ Likes)'
            match = re.search(pattern, content)
            if match:
                matches = match.group()
            else:
                matches = None

            data = {
                "video_url": self.url,
                "title": title,
                "tags": tags,
                "channels": channels, 
                "music": music,
                "place": place,
                "traffic": matches,
                "content": [content],
            }

            with open(self.output_file, 'w') as json_file:
                json.dump(data, json_file, indent=2)

            print(f"Scraped metadata saved to {self.output_file}.\n")

        finally:
            await browser.close()

def main():
    parser = argparse.ArgumentParser(description="Web scraper for specific data using Pyppeteer")
    parser.add_argument("url", help="URL to scrape")
    args = parser.parse_args()

    scraper = TiktokVideoMetadataScraper(args.url)
    asyncio.get_event_loop().run_until_complete(scraper.scrape_data_and_save_to_json())

if __name__ == "__main__":
    main()
