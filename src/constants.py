import enum


class Change(enum.Enum):
    NEGATIVE = 0,
    POSITIVE = 1,
    SAME = 2,
    NEW = 3,
    REMOVED = 4,  # removed from product listing links, no longer monitored product
    IN_STOCK = 5,
    OUT_STOCK = 6
