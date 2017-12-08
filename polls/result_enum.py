from enum import Enum


class StatusEnum(Enum):
    NONE = 1,
    SUCCESS = 2,
    FAILED = 3

status = {
    0: 'NONE',
    2: 'SUCCESS',
    3: 'FAILED'
}
