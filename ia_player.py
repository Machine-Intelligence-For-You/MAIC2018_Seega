from player import Player
# from board import Board
import random
class IA(Player):

    #Team modify this
    name = "IA Name"
    def __init__(self,position, gameSize):
        Player.__init__(self,position, gameSize)


    #Rewrite the abstract method
    def play(self, dethToCover, board, step):
        if step == 0:
            a, b = self.playRandom(board,step)
            return a, b
        elif step == 1:
            a, b, c, d = self.playRandom(board, step)
            return a, b, c, d

    def playOld(self, board,step): #OldPlay
        if(step==0):
            for i in range(self.gameSize):
                for j in range(self.gameSize):
                    if(self.canPlayHere(board,step,i,j)):
                        return (i,j)
        if(step==1):
            for i in range(self.gameSize):
                for j in range(self.gameSize):
                    if(self.canPlayHere(board,step,i,j)):
                        if board[i][j] == self.playerColor:
                            if len(self.getRealsMoves(board,i,j))>0:
                                (c,d)=self.getRealsMoves(board,i,j)[0]
                                return (i,j,c,d)
        return -1

    def playRandom(self, board,step):
        playable=[]
        if(step==0):
            for i in range(self.gameSize):
                for j in range(self.gameSize):
                    if self.canPlayHere(board,step,i,j):
                        playable.append((i,j))
            choix =playable[random.randint(0, len(playable)-1)]
            return choix[0],choix[1]
        if(step==1):
            origins=self.getMovingPiece(board,self.playerColor)
            origin=origins[random.randint(0, len(origins)-1)]
            destinations=self.getRealsMoves(board,origin[0],origin[1])
            destination=destinations[random.randint(0,len(destinations)-1)]
            #print(origin[0],origin[1],destination[0],destination[1])
            return (origin[0],origin[1],destination[0],destination[1])
        return -1
