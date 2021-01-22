from helpers.channel import ChannelManager, gather_meta, gather_stats, gather_video_meta, gather_video_stats
import pymongo
import api_key
import sys

# Channel JSON structure    https://developers.google.com/youtube/v3/docs/channels
# Video JSON structure      https://developers.google.com/youtube/v3/docs/videos

# MongoDB init
connection = pymongo.MongoClient()
youtube = connection.youtube
channels = youtube.channels

# Channel init
channel_id = sys.argv[1].replace("https://www.youtube.com/channel/", "")
manager = ChannelManager(api_key.key, channel_id)
channel = manager.get_channel_statistics()

# Add all channel videos if channel is new
if channels.count_documents({"_id": channel["id"]}) == 0:
    videos = manager.get_channel_video_data()
    for video in videos:
        gathered = gather_video_meta(video, channel)
        gathered["stats"] = [gather_video_stats(video)]
        youtube.videos.update_one({"_id": gathered["_id"]}, {"$set": gathered}, True)

# Prepare data
stats = gather_stats(channel)
meta = gather_meta(channel)

# Update channel
channels.update_one({"_id": channel["_id"]}, {"$set": meta}, True)
channels.update_one({"_id": channel["_id"]}, {"$push": {"stats": stats}})
