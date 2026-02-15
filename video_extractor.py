import os
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate


# ============================================================
# PAGE CONFIG
# =====================================z=======================

st.set_page_config(
    page_title="YouTube Channel Video Extractor",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# PROFESSIONAL GRAY + BLUE THEME
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f1f5f9;  /* Light Gray */
}

/* Title */
h1 {
    color: #1e293b;
    text-align: center;
    font-size: 38px;
    font-weight: 700;
}

/* Card Container */
.block-container {
    background-color: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Input box */
.stTextInput>div>div>input {
    background-color: #ffffff;
    color: #1e293b;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    padding: 10px;
}

/* Input focus */
.stTextInput>div>div>input:focus {
    border: 1px solid #2563eb;
    box-shadow: 0 0 5px #2563eb;
}

/* Button */
.stButton>button {
    background-color: #2563eb;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 25px;
    border: none;
}

.stButton>button:hover {
    background-color: #1d4ed8;
    color: white;
}

/* DataFrame styling */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
    padding: 10px;
}

/* Success message */
.stSuccess {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
}

/* Warning */
.stWarning {
    border-radius: 8px;
}

/* Error */
.stError {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# STEP 1: GET ALL VIDEO IDS
# ============================================================

def get_all_video_ids(channel_id: str) -> list:
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise EnvironmentError("YOUTUBE_API_KEY not found. Set it in environment variables.")

    youtube = build("youtube", "v3", developerKey=api_key)

    video_ids = []
    next_page_token = None

    try:
        while True:
            request = youtube.search().list(
                part="id",
                channelId=channel_id,
                maxResults=50,
                order="date",
                type="video",
                pageToken=next_page_token
            )

            response = request.execute()

            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#video":
                    video_ids.append(item["id"]["videoId"])

            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

        return video_ids

    except HttpError as e:
        raise RuntimeError(f"YouTube API Error while fetching video IDs: {e}")


# ============================================================
# STEP 2: GET VIDEO DETAILS
# ============================================================

def get_video_details(video_ids: list) -> pd.DataFrame:
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise EnvironmentError("YOUTUBE_API_KEY not found.")

    youtube = build("youtube", "v3", developerKey=api_key)

    all_video_data = []

    try:
        for i in range(0, len(video_ids), 50):

            batch_ids = video_ids[i:i + 50]

            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(batch_ids)
            )

            response = request.execute()

            for item in response.get("items", []):

                try:
                    duration_seconds = int(
                        isodate.parse_duration(
                            item["contentDetails"].get("duration", "PT0S")
                        ).total_seconds()
                    )
                except:
                    duration_seconds = 0

                video_data = {
                    "video_id": item.get("id", ""),
                    "title": item["snippet"].get("title", ""),
                    "description": item["snippet"].get("description", ""),
                    "publish_date": item["snippet"].get("publishedAt", ""),
                    "duration_seconds": duration_seconds,
                    "view_count": int(item["statistics"].get("viewCount", 0)),
                    "like_count": int(item["statistics"].get("likeCount", 0)),
                    "comment_count": int(item["statistics"].get("commentCount", 0)),
                    "thumbnail_url": item["snippet"]["thumbnails"]["default"].get("url", "")
                }

                all_video_data.append(video_data)

        return pd.DataFrame(all_video_data)

    except HttpError as e:
        raise RuntimeError(f"YouTube API Error while fetching video details: {e}")


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_all_videos_from_channel(channel_id: str) -> pd.DataFrame:
    video_ids = get_all_video_ids(channel_id)

    if not video_ids:
        return pd.DataFrame()

    video_df = get_video_details(video_ids)

    if not video_df.empty:
        video_df["publish_date"] = pd.to_datetime(
            video_df["publish_date"], errors="coerce"
        )

    return video_df


# ============================================================
# STREAMLIT UI
# ============================================================

st.title("YouTube Channel Video Extractor")

channel_id = st.text_input("Enter YouTube Channel ID")

if st.button("Extract Videos"):

    if not channel_id:
        st.warning("Please enter a valid Channel ID.")
    else:
        with st.spinner("Fetching videos... Please wait"):
            try:
                df = extract_all_videos_from_channel(channel_id)

                if df.empty:
                    st.error("No videos found for this channel.")
                else:
                    st.success(f"Successfully extracted {len(df)} videos")
                    st.dataframe(df, use_container_width=True)

                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="youtube_videos.csv",
                        mime="text/csv"
                    )

            except Exception as e:
                st.error(str(e))
