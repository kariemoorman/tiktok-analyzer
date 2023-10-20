import sys
sys.path.append('/Users/karie/Github/tiktok-teller')

import unittest
from unittest.mock import patch
from src.downloaders.tiktok_downloader import TikTokVideoDownloader 

class TestTikTokVideoDownloader(unittest.TestCase):
    @patch('src.downloaders.tiktok_downloader.launch')
    def test_pyppeteer_tiktok_video_downloader(self, mock_launch):
        url = ["https://www.tiktok.com/@srhoe/video/7288795368760823070"]
        downloader = TikTokVideoDownloader(url)
        downloader.download_tiktok_videos(browser="pyppeteer")
        self.assertEqual(mock_launch.call_count, 1)


if __name__ == '__main__':
    unittest.main()
