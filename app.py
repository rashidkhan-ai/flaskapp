from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

ZRE_FEED = "https://english.zrumbesh.com/feed/"

@app.route("/")
def home():
    return {"message": "ZRumbesh Proxy Running!"}

@app.route("/feed")
def get_feed():
    try:
        r = requests.get(ZRE_FEED, timeout=10)
        r.raise_for_status()
        
        root = ET.fromstring(r.content)
        channel = root.find("channel")

        items = []
        for item in channel.findall("item"):
            items.append({
                "title": item.findtext("title"),
                "link": item.findtext("link"),
                "pubDate": item.findtext("pubDate"),
                "description": item.findtext("description")
            })
        
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)})
