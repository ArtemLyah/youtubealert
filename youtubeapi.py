from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from datetime import datetime
import requests


service = build("youtube", "v3", developerKey="AIzaSyCBIvms7wo-pRvflwinAfP8NuWxarB-6rU")
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

def get_channel_info(url):
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

def check_on_new_video(playlist_id, last_video_id):
    playlist = service.playlistItems().list(part="contentDetails", playlistId=playlist_id, maxResults=10).execute()
    videos = []
    if last_video_id:
        for video in playlist["items"]:
            if video["contentDetails"]["videoId"] != last_video_id:
                videos.append(video["contentDetails"]["videoId"])
            else:
                break
    else:
        videos.append(playlist["items"][0]["contentDetails"]["videoId"])
    return videos
