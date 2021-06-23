import dataclasses as dto

@dto.dataclass
class QuotaInfo:
    api_key: str
    curr_quota: int
    curr_date: int

class YoutubeDataApiOperations():
    LIST = 1
    SEARCH = 100
