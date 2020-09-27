from enum import Enum

VALID_COUNTRY_CODES = ["Australia", "China", "Latvia", "Peru"]


class Segment(Enum):
    FREQUENT = 1
    RECENCY = 2
