#from msilib.schema import SelfReg
from abc import ABC, abstractmethod
from operator import truediv
import random
from unittest import suite
from Card import Card
from Enum import Convention


class Player(ABC):

    def __init__(self, id, partner,team) -> None:
        self._id = id  
        self._partner = partner
        self._points = 0
        self._hand = []
        self._team = team
        self._playedCards={}

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
        self._points += points
    
    def getPoints(self):
        return self._points
    
    def playCardManual(self, card):
        self._hand.remove(card)

    @abstractmethod
    def getInfo(self,currentPlayedCards,trump) -> Card:
        raise NotImplementedError()

    @abstractmethod
    def makePlay(self) -> Card:
        raise NotImplementedError()

# =================================================================================================

class RandomPlayer(Player):

    def __init__(self, id, partner, team) -> None:
        super(RandomPlayer,self).__init__(id, partner,team)

    def getInfo(self,currentPlayedCards,trump):
        return

    def makePlay(self,validCards):
        return random.choice(validCards)
        
# =================================================================================================

class ConventionalPlayer(Player):

    def __init__(self, id, partner, team, socialConvention) -> None:
        super(ConventionalPlayer,self).__init__(id, partner,team)
        self.socialConvention = socialConvention

    def getInfo(self,currentPlayedCards,trump):
        return

    def getSocialConvetion(self):
        return self.socialConvention

    def makePlay(self,validCards, social_convention, trump):
        comparativeCard = validCards[0]
        for card in validCards:
            #checks what card among the valid cards has the highest value and stores that card in the "comparativeCard" variable
            if (social_convention.name == "AlwaysHighestCard"):
                if(card.getCardPoints() > comparativeCard.getCardPoints()):
                    comparativeCard = card

            #checks what card among the valid cards has the lowest value and stores that card in the "comparativeCard" variable
            elif (social_convention.name == "AlwaysLowestCard"):
                if(card.getCardPoints() < comparativeCard.getCardPoints()):
                    comparativeCard = card

            #checks what cards among the valid cards, if any, are trump cards and stores those cards in an auxilary list
            elif ((social_convention.name == "AlwaysHighestTrumpCard") or (social_convention.name == "AlwaysLowestTrumpCard")):
                auxTrumpCardsList = []
                if(card.getSuit() == trump):
                    auxTrumpCardsList.append(card)
        
        #checks among the trump cards which one has the highest value
        if (social_convention.name == "AlwaysHighestTrumpCard"):
            if (auxTrumpCardsList != []):
                comparativeCard = auxTrumpCardsList[0]
                for card in auxTrumpCardsList:
                    if(card.getCardPoints() > comparativeCard.getCardPoints()):
                        comparativeCard = card
            else:
                #if there are no trump cards among the valid cards then the played cards is the same as if the convention was "AlwaysHighestCard"
                new_social_convention = Convention(1)
                self.makePlay(validCards, new_social_convention, trump)

        #checks among the trump cards which one has the lowest value
        if (social_convention.name == "AlwaysLowestTrumpCard"):
            if (auxTrumpCardsList != []):
                comparativeCard = auxTrumpCardsList[0]
                for card in auxTrumpCardsList:
                    if(card.getCardPoints() < comparativeCard.getCardPoints()):
                        comparativeCard = card
            else:
                #if there are no trump cards among the valid cards then the played cards is the same as if the convention was "AlwaysLowestCard"
                new_social_convention = Convention(2)
                self.makePlay(validCards, new_social_convention, trump)


        return comparativeCard