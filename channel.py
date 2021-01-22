from helpers.channel import ChannelManager, gather_meta, gather_stats
import pymongo
import api_key
import sys

# Channel JSON structure https://developers.google.com/youtube/v3/docs/channels

# MongoDB init
connection = pymongo.MongoClient()
youtube = connection.youtube
channels = youtube.channels

# Channel init
channel_id = sys.argv[1].replace("https://www.youtube.com/channel/", "")
manager = ChannelManager(api_key.key, channel_id)
channel = manager.get_channel_statistics()

# Prepare data
stats = gather_stats(channel)
meta = gather_meta(channel)

# Import to MongoDB
channels.update_one({"_id": channel["_id"]}, {"$set": meta}, True)
channels.update_one({"_id": channel["_id"]}, {"$push": {"stats": stats}})
