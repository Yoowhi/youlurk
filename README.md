# YouLurk
Python scripts for gathering YouTube statistics. All data will store in local MongoDB server<br>
Requires `pyfy` and `pymongo` packages

## video.py
Gather information from video and updates mongodb server. Likes, dislikes, views, and rating have history 
Use with argument which is video url<br>
For example:`video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ`