#from msilib.schema import SelfReg
from abc import ABC, abstractmethod
from ast import Raise
from operator import truediv
import random
from unittest import suite
from Card import Card
from Enum import Convention
import copy
import MonteCarlo


class Player(ABC):

    def __init__(self, id) -> None:
        self._id = id  
        self._partner = ''
        self._points = 0
        self._hand = []
        self._deck = []
        self._team = ''
        self._playedCards={}

    def getHand(self):
        return self._hand
    
    def handLen(self):
        return len(self._hand)
    
    def getDeck(self):
        return self._deck

    def toStringList(self,l):
        aux = []
        for c in l:
            aux.append(c.getStringCard())
        return aux


    def getTeam(self):
        return self._team 

    def getStringHand(self):
        i = 0
        returnStr = ''
        for card in self._hand:
            returnStr += str(i) + ":" + card.getStringCard() +'\n'
            i += 1
            
        return returnStr  

    def setTeam(self, team):
        self._team = team

    def setHand(self, hand):
        self._hand = hand
    
    def setDeck(self, deck):
        aux = deck.copy()
        for card in self.getHand():
            aux.remove(card)
        self._deck = aux
    
    def getId(self):
        return self._id

    def setPoints(self,points):
        self._points += points
    
    def resetPoints(self):
        self._points = 0
    
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

    def __init__(self, id) -> None:
        super(RandomPlayer,self).__init__(id)

    def getInfo(self,currentPlayedCards,trump):
        return

    def makePlay(self,validCards):
        return random.choice(validCards)
        
# =================================================================================================

class ConventionalPlayer(Player):

    def __init__(self, id, socialConvention) -> None:
        super(ConventionalPlayer,self).__init__(id)
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

# ================================================================================================================================
class MCTSPlayer (Player):
    def __init__(self, id, nSimulation) -> None:
        super(MCTSPlayer,self).__init__(id)
        self._nSimulation = nSimulation
    
    def getInfo(self,currentPlayedCards,trump):
        return
    
    def trimDeck(self,cardRound):
        for c in cardRound:
            if c in self._deck :
                self._deck.remove(c)

    def makePlay(self,valid_cards,currentPlayedCards,currentSuit, trump):
        cardsPlayed = []
        deck = self.getDeck()
        valid = copy.copy(valid_cards)
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CURRENT DECK UNSEEN: ", len(deck))
        for _, cards in currentPlayedCards.items():
            cardsPlayed.append(cards)
            if cards in deck :
                deck.remove(cards)
        #print("Cards Played So far",len(cardsPlayed))
        state  = MonteCarlo.State(len(cardsPlayed),cardsPlayed,trump,currentSuit)

        root = MonteCarlo.MCTSNode(valid,self.handLen(),deck,state,None,None)
        for i in range(0,self._nSimulation):
            #print("================  newRound  ================\n")
            root.transverseTree()
        #print("ENDED")
        #print(root.pickBestPlay())
        return root.pickBestPlay()