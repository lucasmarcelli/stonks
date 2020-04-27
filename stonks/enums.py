from enum import IntEnum

class ActionEnum(IntEnum):
    BUY = 1
    SELL = 2

class HoldingTypeEnum(IntEnum):
    STOCK = 1
    MUTUAL = 2

class EventTypeEnum(IntEnum):
    TRADE = 1
    BANK = 2

