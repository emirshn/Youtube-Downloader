from pytube import YouTube
from flask import Flask, request
from flask_cors import CORS
import time
from hurry.filesize import size

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "api"


@app.route('/api/youtube')
def youtube():
    url = request.args.get("url")
    if url:
        yt = YouTube(url)
        video = {
            "info": {
                "title": yt.title,
                "author": yt.author,
                "thumbnail": yt.thumbnail_url,
                "description": yt.description,
                "time": time.strftime("%H:%M:%S", time.gmtime(yt.length)),
                "views": yt.views,
                "publish_date": yt.publish_date
            },
            "sources": []
        }
        videos = yt.streams.filter(progressive=True)
        for v in videos:
            video["sources"].append({
                "url": v.url,
                "resolution": v.resolution,
                "size": size(v.filesize)
            })

        return video
