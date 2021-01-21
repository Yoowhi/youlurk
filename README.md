# YouLurk
Python scripts for gathering YouTube statistics. All data will store in local MongoDB server<br>
Requires `pyfy` and `pymongo` packages

## video.py
Gathers information from video and updates mongodb server. Likes, dislikes, views, and rating have history.<br>
<br> 
Use with argument which is video url. For example:<br>`video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ`