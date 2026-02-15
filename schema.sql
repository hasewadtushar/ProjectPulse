CREATE TABLE channels (
    channel_id VARCHAR(100) PRIMARY KEY,
    channel_name VARCHAR(200) NOT NULL,
    description TEXT,
    subscribers BIGINT,
    total_videos INT,
    total_views BIGINT,
    created_date TIMESTAMP,
    thumbnail_url TEXT
);

CREATE TABLE videos (
    video_id VARCHAR(100) PRIMARY KEY,
    channel_id VARCHAR(100) NOT NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    publish_date TIMESTAMP,
    duration INT,
    thumbnail_url TEXT,

    CONSTRAINT fk_channel
        FOREIGN KEY(channel_id)
        REFERENCES channels(channel_id)
        ON DELETE CASCADE
);

CREATE TABLE video_statistics (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(100) UNIQUE NOT NULL,
    views BIGINT,
    likes BIGINT,
    comments BIGINT,

    CONSTRAINT fk_video
        FOREIGN KEY(video_id)
        REFERENCES videos(video_id)
        ON DELETE CASCADE
);
