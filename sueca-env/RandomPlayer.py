#from msilib.schema import SelfReg
from operator import truediv
import random
from unittest import suite
import Player


class RandomPlayer(Player.Player):

    def __init__(self, id, partner,team) -> None:
        super(RandomPlayer,self).__init__(id, partner,team)

    def getInfo(self,currentPlayedCards,trump):
        return

        

    def makePlay(self,validCards):
        return random.choice(validCards)
