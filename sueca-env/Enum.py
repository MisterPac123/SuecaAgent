import enum

class CardSuitEnum(enum.Enum):
    Heart = 1
    Club = 2
    Diamond = 3
    Spade = 4


class Convention(enum.Enum):
    AlwaysHighestCard = 1
    AlwaysLowestCard = 2
    AlwaysHighestTrumpCard = 3
    AlwaysLowestTrumpCard = 4