from email.policy import default
import random
from Card import Card
from Player import Player


card_value =['ACE','SEVEN','KING','QUEEN','JACK','TWO','THREE','FOUR','FIVE','SIX']
card_suit = ['Heart', 'Club', 'Diamond', 'Spades']

def setupSueca():
    players = initPlayers()
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
            card = playerTurn(currentPlayer, currentSuit, turn, currentPlayedCards)
            
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
                    if p.getId == winner:
                        break
                    continue
                p.setPoints(points)
                #TODO check who won the turn
                #put that player as leaded
                #sum points for the team
            


def initPlayers() :
    players = []
    p1 = Player('P1', 'P3')
    p2 = Player('P2', 'P4')
    p3 = Player('P3', 'P1')
    p4 = Player('P4', 'P2')
    players.append(p1)
    players.append(p2)
    players.append(p3)
    players.append(p4)
    return players

def setTrump (suit):
    gameTrump = suit

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
            str_hand = str_hand + crd.getValue() + ' ' + crd.getSuit() + '||'
        str = str_id + ' ' + str_hand
        print(str)


def filter_suit (suit,hand):
    possibleCards = []
    for card in hand:
        if card.suit == suit:
            possibleCards.append(card)
        
    if possibleCards:
        return possibleCards
    else:
        return hand         


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



def main():

    players,gameTrump = setupSueca()
    startGame(players,gameTrump)


    
if __name__ == "__main__":
    main()



