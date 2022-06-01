class Card:
    
    def __init__(self, _suit, _value) -> None:
        self.suit = _suit
        self.value = _value

    
    def getSuit(self) :
        return self.suit

    def getValue(self) :
        return self.value
    
    def getStringCard(self) :
        return self.getSuit() + " " + self.getValue()

    def getCardPoints(self):
        cardValue = self.value
        match cardValue:
            case 'Q':
                return 2
            case 'J':
                return 3
            case 'K':
                return 4
            case 7:
                return 10
            case 'A':
                return 11
            case default:
                return 0