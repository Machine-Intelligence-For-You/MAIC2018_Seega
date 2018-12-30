from abc import ABC, abstractmethod

class Player(ABC):
    name = "Player"
    def __init__(self, position, gameSize):
        self.score=0
        self.position=position
        self.gameSize = gameSize
        color = ["black", "white"]
        self.playerColor = color[position]
        self.origin = None

    @abstractmethod
    def play(self, dethToCover, board, step):
        pass

    def getName(self):
        return self.name


    def getScore(self):
        return self.score
    def setScore(self,s):
        self.score=self.score+s

    def canPlayHere(self, board, step, x, y):
        if step == 0:
            if x == self.gameSize //2 and y == self.gameSize //2:
                return False
            if board[x][y] is None:
                return True
            return False
        if step == 1:
            if board[x][y] is not None:
                if board[x][y] == self.playerColor:
                    self.origin = (x, y)
                    return True
                else:
                    self.origin = None
                return False
            elif board[x][y] is None:
                if self.origin is not None:
                    return True
                return False




    def getPossibleMoves(self, x, y):
        return [(x + a[0], y + a[1]) for a in
                [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if ((0 <= x + a[0] < self.gameSize) and (0 <= y + a[1] < self.gameSize))]

    def getRealsMoves(self,board, x, y):
        moves = []
        for i in self.getPossibleMoves(x,y):
            if board[i[0]][i[1]] is None:
                moves.append(i)
        return moves

    def getMovingPiece(self,board,color):
        i, j = -1, -1
        movingPieces = list()
        for el in board:
            i +=1
            for p in el:
                j +=1
                if self.pieceCanMove(board,(i,j), color):
                    movingPieces.append((i,j))
            j = -1

        return movingPieces



    def getPlayerPiece(self, board):
        playerPieces = []
        for i in range(self.gameSize):
            for j in range(self.gameSize):
                if board[i][j] is not None and board[i][j] == self.playerColor:
                    playerPieces.append((i,j))
        return playerPieces


    def pieceCanMove(self,board, origin, color):
        if board[origin[0]][origin[1]] is not None and board[origin[0]][origin[1]] == color and len(self.getRealsMoves(board, origin[0], origin[1])) > 0:
            return True
        return False
    def isPiece(self,board,x,y):
        if board[x][y] == None:
            return False
        return True


    def hasCaptured(self,board, x, y, color):
        gameSize=len(board)
        advNeighbours = []
        captured =[]
        for i in self.getPossibleMoves(x,y):
            if self.isPiece(board,i[0],i[1]) and board[i[0]][i[1]] != color:
                advNeighbours.append(i)
        if(len(advNeighbours)>0):
            for adv in advNeighbours:
                if adv[0] != gameSize//2 or adv[1] != gameSize//2:
                    if(adv[0] == x):
                        #print("Horizontal")

                        if adv[1]<y and 0 <= y-2 < gameSize and self.isPiece(board,x,y-2) and board[x][y-2] == board[x][y]:
                            #print("ok1")
                            captured.append((x,y-1))

                        if adv[1]>y and 0 <= y+2 < gameSize and self.isPiece(board,x,y+2) and board[x][y+2] == board[x][y]:
                            #print("ok2")
                            captured.append((x,y+1))

                    elif adv[1] == y:
                        ##print("vertical")
                        if adv[0]<x and 0 <= x-2 < gameSize and self.isPiece(board,x-2,y) and board[x-2][y] == board[x][y]:
                            #print("ok3")
                            captured.append((x-1,y))
                        if adv[0]>x and 0 <= x+2 < gameSize and self.isPiece(board,x+2,y) and board[x+2][y] == board[x][y]:
                            #print("ok4")
                            captured.append((x+1,y))
        return captured


    def clone(self,tab):
        copy=[]
        for item in tab:
            temp=[]
            for i in item:
                temp.append(i)
            copy.append(temp)
        return copy


