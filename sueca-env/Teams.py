from Enum import Convention
from Players import RandomPlayer, ConventionalPlayer, MCTSPlayer
import copy

def oldInitPlayers ():
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


def createTeams():

    #AlwaysHighestCardConvention 
    HCC= Convention(1)

    #AlwaysLowestCardConvention
    LCC= Convention(2)

    #AlwaysHighestTrumpCardConvention 
    HTC= Convention(3)

    #AlwaysLowestTrumpCardConvention
    LTC= Convention(4)

    #create Players
    players = [RandomPlayer('Rand'), ConventionalPlayer('HCC', HCC), ConventionalPlayer('LCC', LCC),
    ConventionalPlayer('HTC', HTC),ConventionalPlayer('LTC', LTC), MCTSPlayer("MonteCarlo", 1000)]

    #create all possible unique teams of 2 from players, adds them to a dictionary with the key being their team name: 15 teams
    teams = {}
    for i in range(0, len(players)):
        for i2 in range(i, len(players)):
            p1 = copy.deepcopy(players[i])
            p2 = copy.deepcopy(players[i2])
            teamName = p1.getId() + "-" + p2.getId() 
            teams.update( { teamName : (p1 , p2) } )
    
    return teams