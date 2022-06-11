from email.policy import default
import random
from Card import Card
from Enum import Convention
from Players import RandomPlayer, ConventionalPlayer
from RealPlayer import RealPlayer


card_value =['ACE','SEVEN','KING','QUEEN','JACK','TWO','THREE','FOUR','FIVE','SIX']
card_suit = ['Heart', 'Club', 'Diamond', 'Spades']


# ======================================== SetUp ========================================
def setupSueca():
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
    currentCards = []

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
            
def initPlayers() :
    players = []
    correctInput = False
    while (not correctInput):
        print("\nIndicate what type of players you want:\n RandomPlayers -> 0\n ConventionalPlayers -> 1")
        inputPlayerType = input()
        if (inputPlayerType == "0"):
            correctInput = True
            p1 = RandomPlayer('P1', 'P3','A')
            p2 = RandomPlayer('P2', 'P4','B')
            p3 = RandomPlayer('P3', 'P1','A')
            p4 = RandomPlayer('P4', 'P2','B')

        elif (inputPlayerType == "1"):
            correctInput = True
            correctInput2 = False
            while (not correctInput2):
                print("\nChoose what type of social convention should the players follow\n AlwaysHighestCard -> 1")
                print(" AlwaysLowestCard -> 2\n AlwaysHighestTrumpCard -> 3\n AlwaysLowestTrumpCard -> 4")
                inputConvention = input()
                if(eval(inputConvention) in [1,2,3,4]):
                    correctInput2 = True
                    convention = Convention(eval(inputConvention))
                    print(convention.name)
                    p1 = ConventionalPlayer('P1', 'P3','A', convention)
                    p2 = ConventionalPlayer('P2', 'P4','B', convention)
                    p3 = ConventionalPlayer('P3', 'P1','A', convention)
                    p4 = ConventionalPlayer('P4', 'P2','B', convention)
                else:
                    print("\nInvalid Convention input. Press 0, 1, 2 or 4")
        else:
            print("\nInvalid Player Type input. Press 0 or 1 ")

    players.append(p1)
    players.append(p2)
    players.append(p3)
    players.append(p4)
    return players

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
def getCardInput(currentplayer, turn, currentSuit, currentPlayedCards) :
    valid_cards = []

    if len(currentPlayedCards)>0:
        print('\n###################\nCurrent played cards')
        for playerID in currentPlayedCards:
            print(playerID + '->' + currentPlayedCards[playerID].getStringCard())
        print('\n###################')
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

    playedCard = getCardInput(currentPlayer, turn, currentSuit, currentPlayedCards)
    #playedCard = currentPlayer.getHand()[index]
    currentPlayer.playCardManual(playedCard)
    print(currentPlayer.getId() + " played " + playedCard.getStringCard())
    return playedCard

# ========================================== /REAL PLAYERS ==========================================


# ========================================== SELF PLAYERS ==========================================
#
# The agent will play instead of waiting for input
#
def selfPlayerTurn(currentPlayer, currentSuit, trump, currentPlayedCards):

    playedCard = getValidPlay(currentPlayer, currentSuit, currentPlayedCards, trump)
   # currentPlayer.getInfo(currentPlayedCards,trump)
    currentPlayer.playCardManual(playedCard)
    print(currentPlayer.getId() + " played " + playedCard.getStringCard())
    return playedCard


def getValidPlay(currentplayer, currentSuit, currentPlayedCards, trump) :
    valid_cards = []

    if len(currentPlayedCards)>0:
        print('\n###################\nCurrent played cards')
        for playerID in currentPlayedCards:
            print(playerID + '->' + currentPlayedCards[playerID].getStringCard())
        print('\n###################')
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

# ========================================== SELF PLAYERS ==========================================


#nao assume por agora trunfo
def checkTurnWinner(currentPlayedCards, currentSuit,trump):
    
    winner = ""
    winningCard = None
    points = 0

    for playerKey in currentPlayedCards:

        playedCard = currentPlayedCards[playerKey]
        points += playedCard.getCardPoints()
        print(playerKey + ' -> ' + playedCard.getStringCard())

        cardSuit = playedCard.getSuit()
        if(winningCard == None):
            if (currentSuit != cardSuit):
                print ("dicks out tribolinhas")
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
    teamA = 0
    teamB = 0
    for p in players:
        if p.getTeam() == "A":
            teamA += p.getPoints()
        else:
            teamB += p.getPoints()
    if teamA > teamB:
        print("################### P1 AND P3 won with :", teamA, " ###################")
    elif teamA < teamB:
        print("################### P2 AND P4 won with : ", teamB, " ###################")
    else:
        print("################### DRAW ###################")




def main():
    players,gameTrump = setupSueca()
    startGame(players,gameTrump)
    checkWinningTeam(players)


    
if __name__ == "__main__":
    main()



