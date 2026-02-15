import pandas as pd
from data_processing.channel_extractor import extract_channel_data

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

if __name__ == "__main__":
    channel_id = "UCq0Ut_U_UR4_hGJ8-TbQ_9Q"
    df = extract_channel_data(channel_id)
    print(df)
