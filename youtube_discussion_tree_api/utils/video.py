import dataclasses as dto
@dto.dataclass
class Video:
    id: int
    title : str
    description: str
    channel_name: str
    channel_id: str
    published_at : str