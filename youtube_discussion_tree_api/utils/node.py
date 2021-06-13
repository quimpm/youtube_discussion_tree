import dataclasses as dto
@dto.dataclass
class Node:
    id: int
    author_name: str
    author_id: int
    text: str
    like_count: int
    parent_id: int
    published_at : str