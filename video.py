import pafy
import pymongo
from lib.video import gather_meta, gather_stats
import api_key
import sys


# MongoDB init
connection = pymongo.MongoClient()
youtube = connection.youtube
videos = youtube.videos

# Pufy init
pafy.set_api_key(api_key.key)
url = sys.argv[1]
if url is (None or ""):
    exit()
video = pafy.new(url)

# Gather time!
document = gather_meta(video)
videos.update_one({"_id": video.videoid}, {"$set": document}, True)
stats = gather_stats(video)
videos.update_one({"_id": video.videoid}, {"$push": {"stats": stats}})
