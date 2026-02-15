from googleapiclient.discovery import build

API_KEY = "PASTE_YOUR_API_KEY_HERE"

def get_channel_details(channel_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )

    response = request.execute()

    if response["items"] == []:
        return None

    item = response["items"][0]

    return {
        "name": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "subscribers": item["statistics"]["subscriberCount"],
        "videos": item["statistics"]["videoCount"],
        "views": item["statistics"]["viewCount"],
        "created": item["snippet"]["publishedAt"],
        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
    }
