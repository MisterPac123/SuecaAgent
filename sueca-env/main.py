from email.policy import default
import os
import random
from Card import Card
from Players import RandomPlayer, ConventionalPlayer, MCTSPlayer
from RealPlayer import RealPlayer
from Teams import createTeams
#import numpy as np
#from utils import compare_results
import copy

#from utils import compare_results

card_value =['ACE','SEVEN','KING','QUEEN','JACK','TWO','THREE','FOUR','FIVE','SIX']
card_suit = ['Heart', 'Club', 'Diamond', 'Spades']


# ======================================== SetUp ========================================
"""def setupSueca():
    players= initPlayers()
    deck = buildDeck()
    random.shuffle(deck)
    gameTrump = distributeCards(players, deck)
    printPlayersHands(players)
    print("###  CURRENT TRUMP : ", gameTrump ,"###" )
    return players, gameTrump
  
def startGame(players,trump):
    initialPlayer = random.choice(players)
    playerIndex = players.index(initialPlayer)
    nr_cards_played = 0  
    gameTrump = trump

    for turn in range (1, 11):
        print("#############################################\nCurrent turn:" + str(turn))
        nr_cards_played = 0
        currentSuit = ""
        currentPlayedCards = {}

        while nr_cards_played < 4:

            currentPlayer = players[playerIndex]  # current player is "P'n'"
            #card = playerTurn(currentPlayer, currentSuit, turn, currentPlayedCards)
            card = selfPlayerTurn(currentPlayer, currentSuit, trump, currentPlayedCards)
            currentPlayedCards[currentPlayer.getId()] = card

            if currentSuit == "":
                currentSuit = card.getSuit()

            nr_cards_played += 1
            playerIndex += 1

            if playerIndex >= len(players):
                playerIndex = 0

            if nr_cards_played == 4 :
                winner,points = checkTurnWinner(currentPlayedCards, currentSuit,gameTrump)
                print('Turn winner:' + winner + " \n" + "Round Points:" , points)
                for p in players:
                    if p.getId() == winner:
                        break
                    continue
                p.setPoints(points)

            
        input(" ============== Press Any Key to Proceed ============== \n") 
                
                #put that player as leaded
            
"""


def distributeCards(players, deck):
    aux = deck.copy()
    positions = ["U","D","L","R"]
    i = 0
    for player in players:
        hand = random.sample(aux, 10)
        player.setHand(hand)
        player.setDeck(deck)
        for card in hand:
            aux.remove(card)
    return card.getSuit()    

def buildDeck():
    deck = []
    for suit in card_suit:
        for value in card_value:
            new_card = Card(suit, value)
            deck.append(new_card)
    return deck

def printPlayersHands(players) : 
    for player in players:
        str_id = player.getId()
        hand = player.getHand()
        str_hand = ''
        for crd in hand:
            str_hand = str_hand + crd.getValue() + ' ' + crd.getSuit() + '|| '
        print(str_id + ' ' + str_hand)
        
def filter_suit (suit,hand):
    possibleCards = []
    for card in hand:
        if card.getSuit() == suit: # Changed
            possibleCards.append(card)
        
    if possibleCards:
        return possibleCards
    else:
        return hand         

# ======================================== SetUp ========================================


# ========================================== REAL PLAYERS/ ==========================================
"""def getCardInput(currentplayer, turn, currentSuit, currentPlayedCards) :
    valid_cards = []

    #if len(currentPlayedCards)>0:
    #    print('\n###################\nCurrent played cards')
     #   for playerID in currentPlayedCards:
    #        print(playerID + '->' + currentPlayedCards[playerID].getStringCard())
     #   print('\n###################')
    hand = currentplayer.getHand()
    if currentSuit != "":
        valid_cards = filter_suit(currentSuit, hand)
        
    else:
        valid_cards = hand
    
    index = 0
    for card in valid_cards:
        print(index, ":" , card.getStringCard())
        index+=1
    
    while True:  
        var = int(input("Please choose index of card: "))
        if 0 > var or var > len(valid_cards):
            continue
        return valid_cards[var]
    
def playerTurn(currentPlayer, currentSuit, turn, currentPlayedCards):
    print("player turn being called")
    playedCard = getCardInput(currentPlayer, turn, currentSuit, currentPlayedCards)
    #playedCard = currentPlayer.getHand()[index]
    currentPlayer.playCardManual(playedCard)
    print(currentPlayer.getId() + " played " + playedCard.getStringCard())
    return playedCard"""

# ========================================== /REAL PLAYERS ==========================================






# ========================================== SELF PLAYERS ==========================================
#
# The agent will play instead of waiting for input
#
def selfPlayerTurn(currentPlayer, currentSuit, trump, currentPlayedCards,cardHistory):
    playedCard = getValidPlay(currentPlayer, currentSuit, currentPlayedCards, trump,cardHistory)
   # currentPlayer.getInfo(currentPlayedCards,trump)
    currentPlayer.playCardManual(playedCard)
    #print(currentPlayer.getId() + " played " + playedCard.getStringCard())
    return playedCard


def getValidPlay(currentplayer, currentSuit, currentPlayedCards, trump,cardHistory) :
    valid_cards = []

    #if len(currentPlayedCards)>0:
    #    print('\n###################\nCurrent played cards')
    #    for playerID in currentPlayedCards:
    #        print(playerID + '->' + currentPlayedCards[playerID].getStringCard())
    #    print('\n###################')

    hand = currentplayer.getHand()
    if currentSuit != "":
        valid_cards = filter_suit(currentSuit, hand)
        
    else:
        valid_cards = hand
    
    if (isinstance(currentplayer, RandomPlayer)):
        return currentplayer.makePlay(valid_cards)
    elif (isinstance(currentplayer, ConventionalPlayer)):
        convention = currentplayer.getSocialConvetion()
        return currentplayer.makePlay(valid_cards, convention, trump)
    elif (isinstance(currentplayer, MCTSPlayer)):
        currentplayer.trimDeck(cardHistory)
        return currentplayer.makePlay(valid_cards,currentPlayedCards,currentSuit, trump)


def checkTurnWinner(currentPlayedCards, currentSuit,trump):
    
    winner = ""
    winningCard = None
    points = 0

    for playerKey in currentPlayedCards:

        playedCard = currentPlayedCards[playerKey]
        points += playedCard.getCardPoints()
        #print(playerKey + ' -> ' + playedCard.getStringCard())

        cardSuit = playedCard.getSuit()
        if(winningCard == None):
            if (currentSuit != cardSuit):
                print ("error in function check turn winner")
            winningCard = playedCard
            winner = playerKey
        elif ((cardSuit != winningCard.getSuit() ) and (cardSuit == trump)):
            winningCard = playedCard
            winner = playerKey
        elif (winningCard.getCardPoints() < playedCard.getCardPoints()):
            winningCard = playedCard
            winner = playerKey
    return winner,points

def checkWinningTeam(players):
    teamApoints = 0
    teamBpoints = 0
    for p in players:
        if p.getTeam() == "A":
            teamApoints += p.getPoints()
            p.resetPoints()
        elif p.getTeam() == "B":
            teamBpoints += p.getPoints()
            p.resetPoints()
    return teamApoints, teamBpoints






################################################   NEW   ###############################################################

def startSimulation(players,trump):
    initialPlayer = random.choice(players)
    playerIndex = players.index(initialPlayer)
    nr_cards_played = 0
    cardHistory = []
    

    for turn in range (1, 11):
       # print("#############################################\nCurrent turn:" + str(turn))
        nr_cards_played = 0
        currentSuit = ""
        currentPlayedCards = {}
        teamACounter = 0
        teamBCounter = 0
        print("CARDS PLAYED SO FAR : " ,len(cardHistory), "Turn :" , turn)

        while nr_cards_played < 4:
            currentPlayer = players[playerIndex]  # current player is "NameOfAgentType"
            card = selfPlayerTurn(currentPlayer, currentSuit, trump, currentPlayedCards,cardHistory)
            cardHistory.append(card)

            #currentPlayedCards[currentPlayer.getId()] = card  # PROBLEMA FOUND 10000000%
            currentPlayedCards[id(currentPlayer)] = card  # USES THE ID OF THE OBJECT
            '''Conventional
            if(currentPlayer.getTeam()=="A"):
                teamACounter+=1
                currentPlayedCards[currentPlayer.getTeam()][currentPlayer.getId()+str(teamACounter)] = card 
            else:
                teamBCounter+=1    
                currentPlayedCards[currentPlayer.getTeam()][currentPlayer.getId()+str(teamBCounter)] = card  # PROBLEMA FOUND 10000000%
            '''
            if currentSuit == "":
                currentSuit = card.getSuit()

            nr_cards_played += 1
            playerIndex += 1

            if playerIndex >= len(players):  
               playerIndex = 0

            if nr_cards_played == 4 :
                winner,points = checkTurnWinner(currentPlayedCards, currentSuit,trump)
                for p in players:
                    if id(p) == winner:
                    #if p.getId() == winner:  #changed
                        break
                    continue
                p.setPoints(points)
                playerIndex = players.index(p) # Now after each round, the playerindex is set to the winning player!




def setupMatch(mainDict, teamNameA, teamElemsA, teams, nSimulations):

    for teamNameB, teamElemsB in teams.items():
        teamElemsB[0].setTeam("B")
        teamElemsB[1].setTeam("B")
        counter = 0
        players = [ teamElemsA[0], teamElemsA[1], teamElemsB[0], teamElemsB[1] ]  # PROBLEM !!!!  ALTERING TEAM B FROM THE AUX !!!!!!!!!!!!
        simResultsA = [0] * nSimulations #np.zeros(nSimulations)
        simResultsB = [0] * nSimulations #np.zeros(nSimulations)
        for sim in range(nSimulations):
            deck = buildDeck()
            random.shuffle(deck)
            simTrump = distributeCards(players,deck)
            startSimulation(players, simTrump)
            counter += 1
           # debugPlayer(players)
            teamApoints, teamBpoints = checkWinningTeam(players)
            if((teamApoints + teamBpoints) != 120):
                raise Exception("Round points don't add up to 120")
            simResultsA[sim] = teamApoints
            simResultsB[sim] = teamBpoints

        teamA = mainDict.get(teamNameA)
        teamB = mainDict.get(teamNameB)
        if teamA:
            teamA.update( { teamNameB : simResultsA } )
        else:
            mainDict.update( {teamNameA : { teamNameB : simResultsA } })
        
        if teamB:
            teamB.update( { teamNameA : simResultsB } )
        else:
            mainDict.update( {teamNameB : { teamNameA : simResultsB } })  
    


def printDict(dick):
    for team, subdick in dick.items():
        print("\n \n \n ", "Main team: ", team, ":")
        for vsTeam, result in subdick.items():
            print("results against ", vsTeam, ":", result)

def debugPlayer(players):
    print("=========== Debug to see how many points each player made, thus verifying that the overall values are correct ========== ")
    for p in players:
        print(p.getId(),p.getTeam(), "Points : ", p.getPoints())

'''
def createPlots(dict):
    path= os.path.abspath("plots")
    for key, subdict in dict.items():
        filename = path + "/" + key + ".png"
        compare_results(
        subdict,
        title = "Team " + key + " against other teams",
        colors=["orange", "red", "blue", "green", "yellow",
        "violet", "aqua", "olive", "peru", "salmon",
        "silver", "skyblue","teal", "tomato", "brown"],filename=filename, show = False)
    '''

def main():
    mainDict = {}
    teams = createTeams()
    teamsAux = copy.deepcopy(teams)
    nSimulations = 100
    for teamNameA, teamElemsA in teams.items():
        teamElemsA[0].setTeam("A")
        teamElemsA[1].setTeam("A")
        setupMatch(mainDict, teamNameA, teamElemsA, teamsAux, nSimulations)
        teamsAux.pop(teamNameA)

    printDict(mainDict)

    #createPlots(mainDict)



if __name__ == "__main__":
    main()