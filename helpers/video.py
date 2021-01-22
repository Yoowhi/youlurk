from time import time


def gather_meta(video):
    dictionary = {
        "_id": video.videoid,
        "author": video.author,
        "category": video.category,
        "description": video.description,
        "keywords": video.keywords,
        "length": video.length,
        "published": video.published,
        "title": video.title,
        "username": video.username,
        "timestamp": round(time())
    }
    return dictionary


def gather_stats(video):
    dictionary = {
        "likes": video.likes,
        "dislikes": video.dislikes,
        "rating": video.rating,
        "viewcount": video.viewcount,
        "timestamp": round(time())
    }
    return dictionary
