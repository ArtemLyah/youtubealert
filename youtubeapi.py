from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from datetime import datetime
import requests


service = build("youtube", "v3", developerKey="AIzaSyCBIvms7wo-pRvflwinAfP8NuWxarB-6rU")
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

def get_channel_info(url, headers):
    try:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "lxml")
        meta = soup.find("meta", itemprop="channelId")

        chl_name = soup.find("meta", property="og:title")["content"]
        pl_id = meta["content"][0]+"U"+meta["content"][2:]

        return chl_name, pl_id
    except [requests.HTTPError, AttributeError] as err:
        print(err)
        return "0", "0"

def check_on_new_video(playlist_id, time):
    playlist = service.playlistItems().list(part="contentDetails", playlistId=playlist_id, maxResults=10).execute()
    videos = []
    for video in playlist["items"]:
        videoPublishedAt = datetime.strptime(video["contentDetails"]["videoPublishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        timedelta_sec = (datetime.utcnow() - videoPublishedAt).total_seconds()
        if timedelta_sec/60 < time:
            videos.append([video["contentDetails"]["videoId"], round(timedelta_sec/60)])
    return videos
