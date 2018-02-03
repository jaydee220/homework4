import random


def start_game(a, t, c, g):
    dict = {'A': a, 'T': t, 'C': c, 'G': g}
    player1 = input("Please enter a name for player 1: ")
    player2 = input("Please enter a name for player 2: ")
    winner = ntide_game(dict, player1, player2)
    return print ("Congratulations " +winner+ " you won!")



def ntide_game(n_dict, player1, player2="computer"):

    ml = True  # move left
    tc = 0  # turn count
    done = False
    print("game begins, follwing Nucleotides are set: ", n_dict)
    # set player that begins


    if random.getrandbits(1) == False:
        currplayer = player1
        print (player1, " begins")
    else:
        currplayer = player2
        print(player2, " begins")
    while True:
        # get move of player




        print(n_dict)
        print("total number of Nucleotides: "+ str(sum(n_dict.values())))
        move = input(currplayer + " please enter your move (E.g.: a,2 or c,1) :")

        try:
            n, v = move.split(",")
        except ValueError:
            if move == "" and tc == 1:
                done = True
                ml = False
            else:
                print("Invalid input please try again...")
                continue
        v = int(v)
        n = n.upper()

        if done != True:
            if v > 2 or v < 0 or n not in n_dict.keys() or n_dict[n] == 0:
                print("Invalid move found please try again...")
                continue
            if tc ==1 and v == 2:
                print("Only 1 move possible...")
                continue
            elif v == 2:
                ml = False

                n_dict[n] = n_dict[n]-v
            else:
                n_dict[n] = n_dict[n] - v
                tc += 1
            if tc == 2:
                ml = False


        # check if somebody won (3 out of 4 Ntides are empty)
        # if after my turn there are 3 out of 4 empty entries I won
        zerolist = [zeroes for zeroes in n_dict.values() if zeroes == 0]
        if len(zerolist) == 3:
            return currplayer #return the winning player

        if ml == False:
            if currplayer == player1:
                print("Turn player ", currplayer, " over")
                currplayer = player2
                ml = True
                done = False
                tc = 0

            else:
                print("Turn player ", currplayer, " over")
                currplayer = player1
                ml = True
                done = False
                tc = 0

if __name__ == '__main__':
    print (start_game(5,2,3,1))