#!/usr/bin/python

import os
import re
import time
from datetime import datetime
import pandas as pd 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By




def tiktok_user_video_scraper(url_list, browser='firefox'): 
    
    ''' 
    Definition: 
    For each URL in URL List, extract username, bio, video URLs and associated video captions.
    Write results as CSV.
    
    Input Values:
    URL List: list of tiktok user profile URLs. 
    Browser: Choice of "chrome" or "firefox". Default = 'firefox'.
    
    Example: 
    url_list = ['https://www.tiktok.com/@blitzphd', 'https://www.tiktok.com/@eczachly']
    tiktok_selenium_user_video_scraper(url_list=url_list, browser='chrome')
    
    '''
    
    # DateTime Snapshot
    snapshotdate = datetime.today().strftime('%d-%b-%Y')
    snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')
    # Specify Selenium Driver
    if browser == 'chrome': 
        CHROMEDRIVER_PATH = ""
        CHROME_PATH = ""
        WINDOW_SIZE = "1920,1080"
        options = ChromeOptions()
        options.add_argument("--headless")  
        options.add_argument("--window-size=%s" % WINDOW_SIZE)
        options.binary_location = CHROME_PATH
        prefs = {'profile.managed_default_content_settings.images':2}
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)

    if browser == 'firefox': 
        FIREFOXDRIVER_PATH = ""
        FIREFOX_PATH = ""
        WINDOW_SIZE = "1920,1080"
        options = FirefoxOptions()
        options.add_argument("--headless")  
        options.add_argument("--window-size=%s" % WINDOW_SIZE)

        driver = webdriver.Firefox(options=options)
    
    tiktok_df = pd.DataFrame()
    for url in url_list: 
        ## Scroll to End of Page ##
        # Open URL
        driver.get(url)
        # Set Scroll Pause Rate
        SCROLL_PAUSE_TIME = 25
        # Get Scroll Height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll to Bottom of Page
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            # Wait to Load Page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate New Scroll Height and Compare With Last Scroll Height
            new_height = driver.execute_script("return document.body.scrollHeight")
            # Check for Bottom of Page
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(10)
        
        # Extract Username and Bio
        username = re.sub("https://www.tiktok.com/@","", url)
        bio = driver.find_element(By.XPATH, "//h2[@data-e2e='user-bio']").text
        # Extract Video URLs
        videos = driver.find_elements(By.XPATH, f"//a[contains(@href,'{url}')]") 
        video_list = [i.get_attribute('href') for i in videos]
        # Extract Video Captions
        captions = driver.find_elements(By.XPATH, f"//div[contains(@class,'DivContainer')]/img")
        caption_items = [i.get_attribute('alt') for i in captions]
        caption_list = [re.sub(r"(    |   |  | )created by ([A-Za-z0-9].*?)( [A-Za-z0-9].*?)? with ([A-Za-z0-9].*?)( [A-Za-z0-9].*?)?\'s original sound", "", i) for i in caption_items]
    # Create Output Directory
    os.makedirs(f"../__data/__videos/{username}/{snapshotdate}", exist_ok=True)
    # Create Dataframe 
    tiktok_df['video_link']= video_list
    tiktok_df['video_captions']= caption_list
    tiktok_df['user_bio'] = [bio for i in range(len(tiktok_df))]
    tiktok_df['username'] = [username for i in range(len(tiktok_df))]
    tiktok_df = tiktok_df.iloc[:,[3,2,0,1]]
    # Save DataFrame
    tiktok_df.to_csv(f"../__data/__videos/{username}/{snapshotdate}/{username}_tiktok_videos_{snapshotdatetime}.csv", index=False, sep='\t', encoding='utf-8')
    #Close URL Connection
    driver.close()
    
    
if __name__ == "__main__":
    tiktok_user_video_scraper()
