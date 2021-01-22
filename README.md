# YouLurk
Python scripts for gathering YouTube statistics. All data will be stored in local MongoDB server<br>
Requires `pafy` and `pymongo` packages

## video.py
Gathers information from video and updates mongodb server. Likes, dislikes, views, and rating have history.<br>
<br> 
Use with argument video url. For example:<br>`video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ`

## channel.py
Gathers information about channel. Also gathers all its video if this is new channel