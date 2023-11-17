import time
from youtubesearchpython import *
from yt_dlp import YoutubeDL
import csv
import argparse

class YouTubeSearch:
    def __init__(self, query):
        self.query = query

    def search_youtube(self):
        # custom_search = CustomSearch(self.query, limit=20, searchPreferences="",language="ja", region="JP")
        # custom_search = CustomSearch(self.query, limit=20, searchPreferences="EgJAAQ%253D%253D", language="ja", region="JP")
        custom_search = CustomSearch(self.query, SearchMode.livestreams, limit=5, language="ja", region="JP")
        # custom_search = CustomSearch(self.query, SearchMode.videos, limit=5, language="ja", region="JP")
        return custom_search.result()["result"]

    def export_to_csv(self, data, filename="livestreams.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'URL', 'Channel Name', 'Channel URL', 'Live Viewers', 'Subscribers', 'Likes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({
                    # 'Title': entry.get('title', ''),
                    # 'URL': entry.get('link', ''),
                    # 'Channel Name': entry.get('channel', {}).get('name', ''),
                    # 'Channel URL': entry.get('channel', {}).get('link', ''),
                    # 'Live Viewers': entry.get('viewCount', {}).get('text', ''),
                    # 'Subscribers': entry.get('channel', {}).get('subscribers', ''),
                    # 'Likes': entry.get('like_count', ''),
                    'Title': entry.get('title', ''),
                    'URL': entry.get('link', ''),
                    'Channel Name': entry.get('channel_name', ''),
                    'Channel URL': entry.get('channel_url', ''),
                    'Live Viewers': entry.get('live_viewers', ''),
                    'Subscribers': entry.get('subscribers', ''),
                    'Likes': entry.get('like_count', ''),
                })

    def get_livestream_info(self, url):
        print(f"Getting livestream info from {url}")
        ydl_opts = {
            'skip_download': True,
            'quiet': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'noplaylist': True,
            'format': 'best',
            'youtube_include_dash_manifest': False,
            'dump_single_json': True,
            'default_search': 'auto',
            'simulate': True,
            'forcejson': True,
            'geo_bypass': True,
            'geo_bypass_country': 'JP',
            'prefer_insecure': True,
            'writesubtitles': False,
            'print': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict

    def add_additional_info(self, data):
        newdata = []
        for entry in data:
            title = entry.get('title', '')
            URL = entry.get('link', '')
            channel_name = entry.get('channel', {}).get('name', '')
            channel_url = entry.get('channel', {}).get('link', '')

            url = entry.get('link', '')
            info_dict = self.get_livestream_info(url)
            entry['title'] = title
            entry['URL'] = URL
            entry['channel_name'] = channel_name
            entry['channel_url'] = channel_url
            entry['like_count'] = info_dict.get('like_count', '')
            entry['live_viewers'] = info_dict.get('concurrent_view_count', '')
            entry['subscribers'] = info_dict.get('channel_follower_count', '')
            newdata.append(entry)
        return newdata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search YouTube for livestreams and export data to CSV.")
    parser.add_argument("query", type=str, help="Search query for YouTube.")
    parser.add_argument("--output", type=str, default="livestreams.csv", help="Output CSV filename. Default is 'livestreams.csv'.")
    args = parser.parse_args()

    filename = args.query + time.strftime("%Y%m%d%H%M%S") + ".csv"

    yt_search = YouTubeSearch(args.query)
    data = yt_search.search_youtube()
    newdata = yt_search.add_additional_info(data)
    yt_search.export_to_csv(newdata, args.output)
    print(f"Livestream data exported to {args.output}")