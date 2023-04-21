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
            case 'QUEEN':
                return 2
            case 'JACK':
                return 3
            case 'KING':
                return 4
            case 'SEVEN':
                return 10
            case 'ACE':
                return 11
            case default:
                return 0