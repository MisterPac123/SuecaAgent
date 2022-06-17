from abc import ABC, abstractmethod
from cmath import sqrt
from collections import defaultdict
from Card import Card
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

    def represent(self):
        aux = []
        for c in self.getCardsPlayed():
            aux.append(c.getStringCard())
        return "Player Time to Play: " + str(self.getPlayerTurn()) + " Board: " + str(aux) 




class MCTSNode(ABC):

    def __init__(self,possiblePlays,currentDeck,state,parent,playerPlay) -> None:
        self._possiblePlays = possiblePlays # Hand in root, set of 10 cards in next
        self._nCardsInHand = len(possiblePlays)
        self._playerPlay = playerPlay #no need as its going to be put into the state ! -> see drawing
        self._currentDeck = currentDeck  # remaining deck
        self._nVisits = 0
        self._reward = 0
        self._state = state
        self._children = dict() # card choosen becomes name of the node
        self._parentNode = parent

        
    def UCB(self,q,n,c,t):
        return (q - c *(sqrt(math.log(t)/n))).real

    def Qvalue(self):
        return self.getReward()/self.getVisits()

    def pickBestChild(self):
        best = ""
        bestUCB = 0.0
        for childIndex,childNode in (self._children).items():
            aux = self.UCB(childNode.Qvalue(),childNode.getVisits(),2,self.getVisits())
            if(bestUCB > aux or bestUCB == 0):
                bestUCB = aux
                best = childIndex
        return best

    def pickBestPlay(self):
        bestCard = None 
        bestQ = 0
        #cards = None
        for _,childNode in (self._children).items():
            aux = childNode.Qvalue()
            if(bestQ > aux or bestQ == 0):
                bestQ = aux
                bestCard = childNode.getParentPlay()
     #   print(bestCard.getStringCard())
        return bestCard

    def getParentPlay(self):
        return self._playerPlay

    def transverseTree(self):
       # if(self._parentNode == None):
           # print("==FATHER==")
           # print("     -> Actions left", len(self._possiblePlays),"\n")
           # print("     -> State: ", self._state.represent())
           # print("     -> Visits: ", self._nVisits, " Reward: ", self._reward)
       # else:       
           # print("== SON == ")
           # print("     -> Actions left", len(self._possiblePlays),"\n")
           # print("     -> State: ", self._state.represent())
           # print("     -> Visits: ", self._nVisits, " Reward: ", self._reward)
        if(self.checkTerminal()):
            #print(" == REACHED TERMINAL STATE == ")
            reward = self.getPayOut(self._state)
            self.backPropagation(reward)
        elif (self._nVisits==0):
           # print("$ First Visit $","\n")
            reward = self.rollout()
            self.backPropagation(reward)
        else:
            childIndex = ""
            if(len(self._possiblePlays)!=0):
            #    print("== Expand ==")
                childIndex = self.expand()
            else:
             #   print("== CHOOSE FROM CURRENT CHILDREN ==")
                childIndex= self.pickBestChild()
            child = self.getChildren(childIndex)
            child.transverseTree()


    def expand(self): # expand fase
        possiblePlays = []
        remainDeck = copy.copy(self._currentDeck)
        if(not self.generateLeaf()):
            possiblePlays = random.sample(self._currentDeck, self._nCardsInHand)
        for card in possiblePlays:
            remainDeck.remove(card)
        play = random.choice(self._possiblePlays)
        self._possiblePlays.remove(play)
        newState = State(self._state.getPlayerTurn(),copy.copy(self._state.getCardsPlayed()),self._state.getTrump(),self._state.getSuit()) #copy.deepcopy(self._state)
        newState.addCard(play) # add new card to the list of played cards
        self._children[play.getStringCard()] = MCTSNode(possiblePlays,remainDeck,newState,self,play)
        return play.getStringCard()
    
    def getValidMove(self):
        #use filter_suit(self._possiblePlays,self._state.getSuit())
        return random.choice(self._possiblePlays)

    def rollout(self):
        state = State(self._state.getPlayerTurn(),copy.copy(self._state.getCardsPlayed()),self._state.getTrump(),self._state.getSuit())
        deck = copy.copy(self._currentDeck)
        play = self.getValidMove() # random.choice(self.validateMove(self._possiblePlays,(self._state.getSuit())))  # only can play valid_moves
        state.addCard(play) # add new card to the list of played cards    
        while(state.numberCardsPlayed() < 4):
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

        for i in range(0,state.numberCardsPlayed()):
            points += (playedCards[i]).getCardPoints()
            cardSuit = (playedCards[i]).getSuit()
            if(winningCard == None):
                if (currentSuit != cardSuit):
              #      print ("error in function check turn winner")
                    currentSuit = cardSuit
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
    
    def generateLeaf(self):
        return (self._state.numberCardsPlayed() == 3)

    def visited(self):
        self._nVisits+=1
    
    def setRewards(self, reward):
        self._reward += reward    


#==================================================================================================================================
