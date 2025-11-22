from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class MediaItem:
    message_id: int
    chat_id: int
    file_id: str
    title: str
    series: Optional[str] = None
    season: Optional[int] = None
    episode: Optional[int] = None
    quality: Optional[str] = None
    language: Optional[str] = None
    poster_file_id: Optional[str] = None
    tags: Optional[List[str]] = None

    def to_dict(self):
        d = asdict(self)
        # remove None values
        return {k: v for k, v in d.items() if v is not None}
