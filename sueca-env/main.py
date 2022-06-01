from email.policy import default
import random
from Card import Card
from Player import Player


card_value =['A','K','Q','J','2','3','4','5','6','7']
card_suit = ['Heart', 'Club', 'Diamond', "Spade"]


def setupSueca():
    players = initPlayers()
    deck = buildDeck()
    random.shuffle(deck)
    distributeCards(players, deck)
    printPlayersHands(players)
    return players


def startGame(players):
    initialPlayer = random.choice(players)
    playerIndex = players.index(initialPlayer)
    nr_cards_played = 0  
    currentSuit = 'none'
    currentCards = []

    for turn in range (1, 11):
        print("#############################################\nCurrent turn:" + str(turn))
        nr_cards_played = 0
        currentSuit = 'none'
        currentPlayedCards = {}

        while nr_cards_played < 4:

            currentPlayer = players[playerIndex]
            card = playerTurn(currentPlayer, currentSuit, turn, currentPlayedCards)
            
            currentPlayedCards[currentPlayer.getId()] = card

            if currentSuit == 'none':
                currentSuit = card.getSuit()

            nr_cards_played += 1
            playerIndex += 1

            if playerIndex >= len(players):
                playerIndex = 0

            if nr_cards_played == 4 :
                playerString = checkTurnWinner(currentPlayedCards, currentSuit)
                print('Turn winner:' + playerString)
                
                #playerIndex = players.index(playerString)
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


def distributeCards(players, deck):
    for player in players:
        hand = random.sample(deck, 10)
        player.setHand(hand)
        for card in hand:
            deck.remove(card)


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


def getCardInput(currentplayer, turn, currentSuit, currentPlayedCards) :
    while True:

        if len(currentPlayedCards)>0:
            print('\n###################\nCurrent played cards')
            for keyCard in currentPlayedCards:
                print(keyCard + '->' + currentPlayedCards[keyCard].getStringCard())
            print('\n###################')

        print('\nCurrent player:' + currentplayer.getId() + '\n')

        print(currentplayer.getStringHand())
        var = int(input("Please choose index of card: "))
        
        #check if index is correct
        if(var < 0 or var > (10-turn) ):
            print("\n###################\nIndex out of range\n###################")
            continue

        #check if is a legal move
        elif not(currentplayer.validateMove(var, currentSuit)):
            print("\n###################\nInvalid Move. Player should respect Suit\n###################")
            continue

        else:
            return var



def playerTurn(currentPlayer, currentSuit, turn, currentPlayedCards):

    index = getCardInput(currentPlayer, turn, currentSuit, currentPlayedCards)
    playedCard = currentPlayer.getHand()[index]
    currentPlayer.playCardManual(index)
    print(currentPlayer.getId() + " played " + playedCard.getStringCard())
    return playedCard


#nao assume por agora trunfo
def checkTurnWinner(currentPlayedCards, currentSuit):
    
    winner = ''
    maxValueCard = 0

    for player in currentPlayedCards:
        playedCard = currentPlayedCards[player]
        print(player + ' -> ' + playedCard.getStringCard())
        if (maxValueCard < playedCard.getCardPoints()) and (playedCard.getSuit() == currentSuit):
            maxValueCard = playedCard.getCardPoints()
            winner = player

    return winner



def main():

    players = setupSueca()
    startGame(players)


    
if __name__ == "__main__":
    main()



