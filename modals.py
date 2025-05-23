from pydantic import BaseModel
from typing import Optional

class Reel(BaseModel):
    id: str
    reel_url: str
    video_url: Optional[str]
    thumbnail_url: Optional[str]
    caption: Optional[str]
    posted_at: Optional[str]
    views: Optional[int]
    likes: Optional[int]
    comments: Optional[int]