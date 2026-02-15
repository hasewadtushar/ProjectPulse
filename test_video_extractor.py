import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_processing.video_extractor import extract_all_videos_from_channel

channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

df = extract_all_videos_from_channel(channel_id)

print(df.head())
print("Total Videos:", len(df))
