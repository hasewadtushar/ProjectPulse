import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def extract_channel_data(channel_id: str) -> pd.DataFrame:
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise EnvironmentError("YOUTUBE_API_KEY not found")

    youtube = build("youtube", "v3", developerKey=api_key)

    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        # ✅ SAFE CHECK
        if "items" not in response or len(response["items"]) == 0:
            raise ValueError("Invalid Channel ID or API returned no data")

        item = response["items"][0]

        data = {
            "channel_id": channel_id,
            "channel_name": item["snippet"]["title"],
            "channel_description": item["snippet"]["description"],
            "subscriber_count": int(item["statistics"].get("subscriberCount", 0)),
            "total_videos": int(item["statistics"].get("videoCount", 0)),
            "total_views": int(item["statistics"].get("viewCount", 0)),
            "channel_created_date": item["snippet"]["publishedAt"],
            "channel_thumbnail_url": item["snippet"]["thumbnails"]["default"]["url"]
        }

        return pd.DataFrame([data])

    except HttpError as e:
        raise RuntimeError(f"YouTube API Error: {e}")

    except Exception as e:
        raise RuntimeError(f"Unexpected Error: {e}")
