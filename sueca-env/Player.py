#from msilib.schema import SelfReg
from abc import ABC, abstractmethod
from operator import truediv
from random import random
from unittest import suite
from Card import Card


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
        
