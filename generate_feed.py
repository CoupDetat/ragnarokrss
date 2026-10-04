import os
import html
import requests
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, ElementTree

API_KEY = os.environ["YOUTUBE_API_KEY"]

SEARCH_QUERY = "ragnarok woe"

MAX_RESULTS = 25

API_URL = "https://www.googleapis.com/youtube/v3/search"

params = {
    "part": "snippet",
    "q": SEARCH_QUERY,
    "type": "video",
    "order": "date",
    "maxResults": MAX_RESULTS,
    "key": API_KEY,
}

response = requests.get(API_URL, params=params, timeout=30)

if response.status_code != 200:
    print("YouTube API error:")
    print(response.text)
    response.raise_for_status()

data = response.json()

rss = Element(
    "rss",
    {
        "version": "2.0",
        "xmlns:media": "http://search.yahoo.com/mrss/"
    }
)

channel = SubElement(rss, "channel")

SubElement(channel, "title").text = "Ragnarok WOE - YouTube Search"

SubElement(channel, "description").text = (
    "Latest YouTube videos matching the search: ragnarok woe"
)

SubElement(
    channel,
    "link"
).text = "https://www.youtube.com/results?search_query=ragnarok+woe"

SubElement(
    channel,
    "lastBuildDate"
).text = datetime.now(timezone.utc).strftime(
    "%a, %d %b %Y %H:%M:%S GMT"
)

for item in data.get("items", []):

    video_id = item["id"]["videoId"]
    snippet = item["snippet"]

    title = snippet.get("title", "")
    description = snippet.get("description", "")
    channel_title = snippet.get("channelTitle", "")
    published = snippet.get("publishedAt", "")

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    rss_item = SubElement(channel, "item")

    SubElement(rss_item, "title").text = title

    SubElement(rss_item, "description").text = description

    SubElement(rss_item, "link").text = video_url

    SubElement(rss_item, "guid").text = video_id

    SubElement(rss_item, "author").text = channel_title

    SubElement(rss_item, "pubDate").text = published

    thumbnail = SubElement(
        rss_item,
        "{http://search.yahoo.com/mrss/}thumbnail"
    )

    thumbnail.set(
        "url",
        f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    )

tree = ElementTree(rss)

tree.write(
    "feed.xml",
    encoding="utf-8",
    xml_declaration=True
)

print(f"Created RSS feed with {len(data.get('items', []))} videos.")
