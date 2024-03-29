import json
import requests
from tqdm import tqdm
from time import time


def gather_meta(channel):
    channel["_id"] = channel["id"]
    channel["timestamp"] = round(time())
    del channel["id"]
    del channel["kind"]
    del channel["etag"]
    return channel


def gather_stats(channel):
    statistics = channel["statistics"]
    del channel["statistics"]
    statistics["timestamp"] = round(time())
    return statistics


def gather_video_meta(video, channel):
    dictionary = {
        "_id": video["id"],
        "author": video["snippet"]["channelTitle"],
        "category": video["snippet"]["categoryId"],
        "description": video["snippet"]["description"],
        # "keywords": video["brandingSettings"]["channel"][],
        # "length": video.length,
        "published": video["snippet"]["publishedAt"],
        "title": video["snippet"]["title"],
        "username": channel["snippet"]["customUrl"],
        "timestamp": round(time()),
        "channel_id": video["snippet"]["channelId"],

    }
    return dictionary


def gather_video_stats(video):
    stats = video["statistics"]
    dictionary = {
        "likes": stats["likeCount"],
        "dislikes": stats["dislikeCount"],
        # "rating": video.rating,
        "viewcount": stats["viewCount"],
        "comments": stats["commentCount"],
        "favorites": stats["favoriteCount"],
        "timestamp": round(time())
    }
    return dictionary


# This is a modified version of this: https://github.com/python-engineer/youtube-analyzer
class ChannelManager:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

    def extract_all(self):
        return (self.get_channel_statistics(),
                self.get_channel_video_data())

    def get_channel_statistics(self):
        """Extract the channel statistics"""
        print('get channel statistics...')
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics,contentOwnerDetails,topicDetails,brandingSettings,snippet&id={self.channel_id}&key={self.api_key}'
        pbar = tqdm(total=1)

        json_url = requests.get(url)
        data = json.loads(json_url.text)["items"][0]

        self.channel_statistics = data
        pbar.update()
        pbar.close()
        return data

    def get_channel_video_data(self):
        "Extract all video information of the channel"
        print('get video data...')
        channel_videos, channel_playlists = self._get_channel_content()

        parts = ["snippet", "statistics"]
        videos = []
        for video_id in tqdm(channel_videos):
            videos.append(self._get_single_video_data(video_id, parts))
            # for part in parts:
            #     data = self._get_single_video_data(video_id, part)
            #     channel_videos[video_id].update(data)
        self.video_data = videos
        return videos

    def _get_single_video_data(self, video_id, parts):
        parts = ",".join(parts)
        url = f"https://www.googleapis.com/youtube/v3/videos?part={parts}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0]
        except KeyError as e:
            print(f'Error! Could not get video data: \n{data}')
            data = dict()
        return data

    def _get_channel_content(self, limit=None, check_all_pages=True):
        """
        Extract all videos and playlists, can check all available search pages
        channel_videos = videoId: title, publishedAt
        channel_playlists = playlistId: title, publishedAt
        return channel_videos, channel_playlists
        """
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet,id&order=date"
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)

        vid, pl, npt = self._get_channel_content_per_page(url)
        idx = 0
        while (check_all_pages and npt is not None and idx < 10):
            nexturl = url + "&pageToken=" + npt
            next_vid, next_pl, npt = self._get_channel_content_per_page(nexturl)
            vid.update(next_vid)
            pl.update(next_pl)
            idx += 1

        return vid, pl

    def _get_channel_content_per_page(self, url):
        """
        Extract all videos and playlists per page
        return channel_videos, channel_playlists, nextPageToken
        """
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()
        channel_playlists = dict()
        if 'items' not in data:
            print('Error! Could not get correct channel data!\n', data)
            return channel_videos, channel_videos, None

        nextPageToken = data.get("nextPageToken", None)

        item_data = data['items']
        for item in item_data:
            try:
                kind = item['id']['kind']
                published_at = item['snippet']['publishedAt']
                title = item['snippet']['title']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = {'publishedAt': published_at, 'title': title}
                elif kind == 'youtube#playlist':
                    playlist_id = item['id']['playlistId']
                    channel_playlists[playlist_id] = {'publishedAt': published_at, 'title': title}
            except KeyError as e:
                print('Error! Could not extract data from item:\n', item)

        return channel_videos, channel_playlists, nextPageToken

    def dump(self):
        """Dumps channel statistics and video data in a single json file"""
        if self.channel_statistics is None or self.video_data is None:
            print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
            return

        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics,
                                        "video_data": self.video_data}}

        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = channel_title.replace(" ", "_").lower()
        filename = channel_title + '.json'
        with open(filename, 'w') as f:
            json.dump(fused_data, f, indent=4)

        print('file dumped to', filename)