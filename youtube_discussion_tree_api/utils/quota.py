import dataclasses as dto

@dto.dataclass
class QuotaController:
    api_key: str
    curr_quota: int
    curr_date: int

class QuotaOperations():
    LIST = 1
    SEARCH = 100
