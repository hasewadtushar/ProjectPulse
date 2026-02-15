from sqlalchemy import Column, String, Text, BigInteger, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db_connection import engine

Base = declarative_base()

class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(String(100), primary_key=True)
    channel_name = Column(String(200), nullable=False)
    description = Column(Text)
    subscribers = Column(BigInteger, default=0)
    total_videos = Column(Integer, default=0)
    total_views = Column(BigInteger, default=0)
    created_date = Column(TIMESTAMP)
    thumbnail_url = Column(Text)

    videos = relationship("Video", back_populates="channel")


class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String(100), primary_key=True)
    channel_id = Column(String(100), ForeignKey("channels.channel_id", ondelete="CASCADE"))
    title = Column(String(300), nullable=False)
    description = Column(Text)
    publish_date = Column(TIMESTAMP)
    duration = Column(Integer)
    thumbnail_url = Column(Text)

    channel = relationship("Channel", back_populates="videos")
    statistics = relationship("VideoStatistics", back_populates="video", uselist=False)


class VideoStatistics(Base):
    __tablename__ = "video_statistics"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String(100), ForeignKey("videos.video_id", ondelete="CASCADE"), unique=True)
    views = Column(BigInteger, default=0)
    likes = Column(BigInteger, default=0)
    comments = Column(BigInteger, default=0)

    video = relationship("Video", back_populates="statistics")


# Create tables
Base.metadata.create_all(bind=engine)
