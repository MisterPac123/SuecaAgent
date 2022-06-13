from email.policy import default
from os import abort
import random
from Card import Card
from Players import RandomPlayer, ConventionalPlayer
from RealPlayer import RealPlayer
from Teams import createTeams
from utils import compare_results
import copy

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
    for player in players:
        # select trump suit
        #
        hand = random.sample(deck, 10)
        player.setHand(hand)
        for card in hand:
            deck.remove(card)
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
        if card.suit == suit:
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
def selfPlayerTurn(currentPlayer, currentSuit, trump, currentPlayedCards):
    playedCard = getValidPlay(currentPlayer, currentSuit, currentPlayedCards, trump)
   # currentPlayer.getInfo(currentPlayedCards,trump)
    currentPlayer.playCardManual(playedCard)
  #  print(currentPlayer.getId() + " played " + playedCard.getStringCard())
    return playedCard


def getValidPlay(currentplayer, currentSuit, currentPlayedCards, trump) :
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
    teamBpoints  = 0
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
    gameTrump = trump

    for turn in range (1, 11):
       # print("#############################################\nCurrent turn:" + str(turn))
        nr_cards_played = 0
        currentSuit = ""
        currentPlayedCards = {}

        while nr_cards_played < 4:

            currentPlayer = players[playerIndex]  # current player is "P'n'"
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
                for p in players:
                    if p.getId() == winner:
                        break
                    continue
                p.setPoints(points)




def setupMatch(mainDict, teamNameA, teamElemsA, teams, nSimulations):

    for teamNameB, teamElemsB in teams.items():
        teamElemsB[0].setTeam("B")
        teamElemsB[1].setTeam("B")
        counter = 0
        players = [ teamElemsA[0], teamElemsA[1], teamElemsB[0], teamElemsB[1] ]
        simResultsA = []
        simResultsB = []
        while counter < nSimulations:
            deck = buildDeck()
            random.shuffle(deck)
            simTrump = distributeCards(players,deck)
            startSimulation(players, simTrump)
            counter += 1
            teamApoints, teamBpoints = checkWinningTeam(players)
            if((teamApoints + teamBpoints) != 120):
                print("\nfuckkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk\n")
            simResultsA.append(teamApoints)
            simResultsB.append(teamBpoints)

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


def main():

    mainDict = {}
    teams = createTeams()
    teamsAux = copy.deepcopy(teams)
    nSimulations = 2
    for teamNameA, teamElemsA in teams.items():
        teamElemsA[0].setTeam("A")
        teamElemsA[1].setTeam("A")
        setupMatch(mainDict, teamNameA, teamElemsA, teamsAux, nSimulations)
        teamsAux.pop(teamNameA)

    printDict(mainDict)



if __name__ == "__main__":
    main()