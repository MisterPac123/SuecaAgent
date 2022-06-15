from abc import ABC, abstractmethod
from cmath import sqrt
from collections import defaultdict
import copy
import random
import math

class State:
    def __init__(self,turn,cards,trump,suit) -> None:
        self._playerTurn = turn
        self._cards = cards
        self._trump = trump
        self._suit = suit


    def getPlayerTurn(self):
        return self._playerTurn
    
    def getCardsPlayed(self):
        return self._cards
    
    def numberCardsPlayed(self):
        return len(self._cards)
    
    def getSuit(self):
        return self._suit
    
    def getTrump(self):
        return self._trump

    def addCard(self,card):
        self._cards.append(card)




class MCTSNode(ABC):

    def __init__(self,possiblePlays,currentDeck,state,parent) -> None:
        self._possiblePlays = possiblePlays # Hand in root, set of 10 cards in next
        self._nCardsInHand = len(possiblePlays)
        # self._playerPlay = playerPlay no need as its going to be put into the state ! -> see drawing
        self._currentDeck = currentDeck  # remaining deck
        self._nVisits = 0
        self._reward = 0
        self._state = state
        self._children = dict() # card choosen becomes name of the node
        self._parentNode = parent

        
    def UCB(self,q,n,c,t):
        return q - c *(sqrt(math.log(t)/n))

    def Qvalue(self):
        return self.getReward()/self.getVisits()

    def pickBestChild(self):
        best = ""
        bestUCB = 0 
        for childIndex,childNode in (self._children).items():
            aux = self.UCB(childNode.Qvalue(),childNode.getVisits(),2,self.getVisits())
            if(bestUCB > aux or bestUCB == 0):
                bestUCB = aux
                best = childIndex
        return best

    def transverseTree(self):
        if (self._nVisits==0):
            self.rollout()
        else:
            childIndex = ""
            if(self._possiblePlays!=0):
                childIndex = self.expand()
            else:
                childIndex= self.pickBestChild(self)
            child = self.getChildren(childIndex)
            child.transverseTree()


    def expand(self): # expand fase
        possiblePlays = random.sample(self._currentDeck, len(self._nCardsInHand))
        remainDeck = copy.deepcopy(self._currentDeck)
        for card in possiblePlays:
            (remainDeck).remove(card)
        if(self._possiblePlays):
            play = random.choice(self._possiblePlays)
            self._possiblePlays.remove(play)
            newState = copy.deepcopy(self._state)
            newState.addCard(play) # add new card to the list of played cards
            self._children[play.getStringCard()] = MCTSNode(possiblePlays,remainDeck,newState,self)
        return play.getStringCard()
    
    def getValidMove(self):
        #use filter_suit(self._possiblePlays,self._state.getSuit())
        return random.choice(self._possiblePlays)

    def rollout(self):
        state = copy.deepcopy(self._state)
        deck = copy.deepcopy(self._currentDeck)
        play = self.getValidMove() # random.choice(self.validateMove(self._possiblePlays,(self._state.getSuit())))  # only can play valid_moves
        state.addCard(play) # add new card to the list of played cards    
        while((state.numberCardsPlayed()) != 4):
                card = random.choice(deck)
                deck.remove(card)
                state.addCard(card)
        
        return self.getPayOut(state) 

    def getPayOut(self,state):
        winner = ""
        winningCard = None
        points = 0
        trump = state.getTrump()
        currentSuit = state.getSuit()
        playedCards = state.getCardsPlayed()
        playerPos = state.getPlayerTurn()

        for i in range(0,len(playedCards)):
            points += (playedCards[i]).getCardPoints()
            cardSuit = (playedCards[i]).getSuit()
            if(winningCard == None):
                if (currentSuit != cardSuit):
                    print ("error in function check turn winner")
                winningCard = (playedCards[i])
                winner = i
            elif ((cardSuit != winningCard.getSuit() ) and (cardSuit == trump)):
                winningCard = (playedCards[i])
                winner = i
            elif (winningCard.getCardPoints() < (playedCards[i]).getCardPoints()):
                winningCard = (playedCards[i])
                winner = i
        
        if(winner == playerPos or winner == (playerPos+2)%4):
            return points
        else:
            return 0

    def backPropagation(self,reward):
        self.visited()
        self.setRewards(reward)
        if(self._parentNode):
            (self._parentNode).backPropagation(reward)
        return



    def getChildren(self,childIndex):
        return self._children[childIndex]

    def getReward(self):
        return self._reward

    def getVisits(self):
        return self._nVisits

    def getState(self):
        return self._state
    
    def checkTerminal(self):
        return (self._state.numberCardsPlayed() == 4)

    def visited(self):
        self._nVisits+=1
    
    def setRewards(self, reward):
        self._reward += reward    


#==================================================================================================================================
