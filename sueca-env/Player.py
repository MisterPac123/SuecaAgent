from msilib.schema import SelfReg
from operator import truediv
from random import random
from unittest import suite


class Player:

    hand = []

    def __init__(self, _id, _partner,) -> None:
        self.id = _id  
        self.partner = _partner

    def getHand(self):
        return self.hand
    
    def getStringHand(self):
        i = 0
        returnStr = ''
        for card in self.hand:
            returnStr += str(i) + ":" + card.getStringCard() +'\n'
            i += 1
            
        return returnStr  


    def setHand(self, _hand):
        self.hand = _hand
    
    def getId(self):
        return self.id
    
    def playCardManual(self, pos):
        card = self.hand[pos]
        self.hand.remove(card)
        return card


    def playCardStrategy (self, strategy, initialSuit):
        match strategy:
            case 'random' :
                card = self.playRandomCard(initialSuit)
                return card

            case default:
                card = self.playRandomCard(initialSuit)
                return card


    def playRandomCard(self, initialSuit):
        if(initialSuit == 'none'):
            possibleCards = self.hand
        else:
            possibleCards = self.filterSuitCards(initialSuit, self.hand)

        #cards with the corresponding suit in hand
        if len(possibleCards):
            card = random.choice(possibleCards)

        #no cards with the corresponding suit in hand
        else:
            card = random.choice(self.hand)

        self.hand.remove(card)
        return card


    def filterSuitCards(self, initialSuit, hand):
        possibleCards = []
        for card in hand:
            if card.suit == initialSuit:
                possibleCards.append(card)
        
        return possibleCards
    


    def validateMove(self, index, currentSuit):
        if currentSuit == 'none':
            return True

        possibleCards = self.filterSuitCards(currentSuit, self.hand)
        card = self.hand[index]
        if len(possibleCards) == 0:
            return True

        else:
            if card in possibleCards:
                return True
            else:
                return False
        
