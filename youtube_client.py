import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv('.gitenv')

API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_youtube_client():
    if not API_KEY:
        raise ValueError('YouTube API key not found')

    youtube = build(
        serviceName='youtube',
        version='v3',
        developerKey=API_KEY
    )
    return youtube

def get_channel_details(channel_id):
    try:
        youtube = get_youtube_client()
        request = youtube.channels().list(
            part='snippet,statistics,contentDetails',
            id=channel_id
        )
        return request.execute()
    except HttpError as e:
        raise RuntimeError(f'YouTube API error: {e}')
