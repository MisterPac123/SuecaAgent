#from msilib.schema import SelfReg
from operator import truediv
from random import random
from unittest import suite


class RealPlayer:

    hand = []

    def __init__(self, id, partner,team) -> None:
        self._id = id  
        self._partner = partner
        self._points = 0
        self._team = team

    def getHand(self):
        return self._hand
    
    def getTeam(self):
        return self._team 
    
    def getStringHand(self):
        i = 0
        returnStr = ''
        for card in self._hand:
            returnStr += str(i) + ":" + card.getStringCard() +'\n'
            i += 1
            
        return returnStr  


    def setHand(self, hand):
        self._hand = hand
    
    def getId(self):
        return self._id

    def setPoints(self,points):
        self._points = points
    
    def getPoints(self):
        return self._points
    
    def playCardManual(self, card):
        self._hand.remove(card)


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
            possibleCards = self._hand
        else:
            possibleCards = self.filterSuitCards(initialSuit, self._hand)

        #cards with the corresponding suit in hand
        if len(possibleCards):
            card = random.choice(possibleCards)

        #no cards with the corresponding suit in hand
        else:
            card = random.choice(self._hand)

        self._hand.remove(card)
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
        card = self._hand[index]
        if len(possibleCards) == 0:
            return True

        else:
            if card in possibleCards:
                return True
            else:
                return False
        
