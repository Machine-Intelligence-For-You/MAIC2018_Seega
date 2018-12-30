# Created by HaroldKS at 21/08/2018
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from panel import Panel
from piece import Piece
from util import Trace
from ia_player import IA
import time
#Maybe Here have to delete inheritance from QWidget. Have to see that


class RulesGame:
    def __init__(self):
        self.step=0
        self.i = 0
        self.seedOnBoard=0
        self.nSeedPutOnStep0=0
        self.origin = None
        self.color = ["black", "white"]
        self.no_win = 0
        # super(GameWindow, self).__init__(parent)
    def canPlayHere(self,x,y):
        if(self.step==0):
            if((x == gameSize//2 and y == gameSize//2)):
                return False
            if((game.board.squares[x][y].isPiece())==False):
                return True
            return False
        if(self.step==1):
            if game.board.squares[x][y].isPiece():
                if game.board.currentPlayer == game.board.squares[x][y].piece.getPlayer():
                    self.origin = (x, y)
                    return True
                else:
                    self.origin = None
                return False
            elif not game.board.squares[x][y].isPiece():
                if self.origin is not None:
                    return True
                return False

    def getPossibleMoves(self, x, y):
        return [(x + a[0], y + a[1]) for a in
                [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if ((0 <= x + a[0] < gameSize) and (0 <= y + a[1] < gameSize))]

    def getRealsMoves(self, x, y):
        moves = []
        for i in self.getPossibleMoves(x,y):
            if not game.board.squares[i[0]][i[1]].isPiece():
                # game.board.squares[i[0]][i[1]].setBackgroundColor("green")
                moves.append(i)
        return moves

    def getMovingPiece(self, color):
        i, j = -1, -1
        movingPieces = list()
        for el in game.board.squares:
            i +=1
            for p in el:
                j +=1
                if self.pieceCanMove((i,j), color):
                    movingPieces.append((i,j))
            j = -1
        return movingPieces

    def getPlayerPiece(self, player):
        playerPieces = []
        for i in range(gameSize):
            for j in range(gameSize):
                if game.board.squares[i][j].isPiece() and game.board.squares[i][j].piece.getColor() == game.board.color[player]:
                    playerPieces.append((i,j))
        return playerPieces


    def hasCaptured(self, x, y, color):
        advNeighbours = []
        captured =[]
        for i in self.getPossibleMoves(x,y):
            if game.board.squares[i[0]][i[1]].isPiece() and game.board.squares[i[0]][i[1]].piece.getColor() != color:
                advNeighbours.append(i)
        if(len(advNeighbours)>0):
            for adv in advNeighbours:
                if adv[0] != gameSize//2 or adv[1] != gameSize//2:
                    if(adv[0] == x):
                        print("Horizontal")
                        if adv[1]<y and 0 <= y-2 < gameSize and game.board.squares[x][y-2].isPiece() and game.board.squares[x][y-2].piece.getColor() == game.board.squares[x][y].piece.getColor():
                            print("ok1")
                            captured.append((x,y-1))
                        if adv[1]>y and 0 <= y+2 < gameSize and game.board.squares[x][y+2].isPiece() and game.board.squares[x][y+2].piece.getColor() == game.board.squares[x][y].piece.getColor():
                            print("ok2")
                            captured.append((x,y+1))

                    elif adv[1] == y:
                        print("vertical")
                        if adv[0]<x and 0 <= x-2 < gameSize and game.board.squares[x-2][y].isPiece() and game.board.squares[x-2][y].piece.getColor() == game.board.squares[x][y].piece.getColor():
                            print("ok3")
                            captured.append((x-1,y))
                        if adv[0]>x and 0 <= x+2 < gameSize and game.board.squares[x+2][y].isPiece()and game.board.squares[x+2][y].piece.getColor() == game.board.squares[x][y].piece.getColor():
                            print("ok4")
                            captured.append((x+1,y))
        return captured


    def pieceCanMove(self, origin, color):
        if game.board.squares[origin[0]][origin[1]].isPiece() and game.board.squares[origin[0]][origin[1]].piece.getColor() == color and len(self.getRealsMoves(origin[0], origin[1])) > 0:
            return True
        return False

    def isStuck(self, color):

        if not self.getMovingPiece(color):
            return True
        return False



    def play(self,x,y):
        if game.gameOneGoing:
            if(self.step==0):
                if(self.canPlayHere(x,y)==True):
                    if(game.board.currentPlayer==0):
                        game.board.squares[x][y].setPiece(Piece(0, "black"))
                        game.trace.add_action(game.board.currentPlayer, (x, y), self.step, game.board.getListBoard(), game.board.score)
                        self.seedOnBoard=self.seedOnBoard+1
                        self.nSeedPutOnStep0+=1
                        if(self.nSeedPutOnStep0==2):
                            game.board.currentPlayer=(game.board.currentPlayer+1)%2
                            self.nSeedPutOnStep0=0
                    elif(game.board.currentPlayer==1):
                        game.board.squares[x][y].setPiece(Piece(1,"white"))
                        game.trace.add_action(game.board.currentPlayer, (x, y), self.step, game.board.getListBoard(), game.board.score)
                        self.seedOnBoard=self.seedOnBoard+1
                        self.nSeedPutOnStep0+=1
                        if(self.nSeedPutOnStep0==2):
                            game.board.currentPlayer=(game.board.currentPlayer+1)%2
                            self.nSeedPutOnStep0=0
                    game.panel.updateCurrentPlayer()
                putLim=game.board.gameSize*game.board.gameSize-1
                if(self.seedOnBoard==putLim):
                    self.step=(self.step+1)%2
                    game.board.currentPlayer=(game.board.currentPlayer+1)%2
                    game.panel.updateCurrentPlayer()

                if self.seedOnBoard == putLim and self.isStuck(self.color[game.board.currentPlayer]):
                    game.board.currentPlayer = (game.board.currentPlayer+1)%2
                    game.panel.updateCurrentPlayer()


            elif(self.step==1):
                if game.board.currentPlayer == 0:

                    if(self.canPlayHere(x, y)):
                        print(self.isStuck((self.color[game.board.currentPlayer])), self.color[game.board.currentPlayer])
                        game.board.setDefaultColors()
                        # game.board.squares[x][y].setBackgroundColor("blue")
                        moves = self.getRealsMoves(x, y)
                        print("Actual move",(x,y), "Possible Moves",moves, "Origin", self.origin)
                        if self.origin is not None and (x,y) in self.getRealsMoves(self.origin[0], self.origin[1]):
                            self.move(self.origin, (x,y), game.board.currentPlayer)
                            score = game.board.score
                            game.trace.add_action(game.board.currentPlayer, (self.origin, (x,y)), self.step, game.board.getListBoard(), score)
                            game.board.setDefaultColors()
                            print("Here")
                            tempOrigin = self.origin
                            self.origin = None
                            captured = self.hasCaptured(x, y, self.color[game.board.currentPlayer])
                            print(captured)
                            if(len(captured)>0):
                                self.no_win = 0
                                for pos in captured:
                                    game.board.squares[pos[0]][pos[1]].removePiece()
                                    game.board.score[game.board.currentPlayer] += 1
                            else:
                                self.no_win += 1
                            print("Joueur 0", game.board.score[game.board.currentPlayer])
                            game.panel.updateScore(game.board.score)

                            if self.checkForEnd():
                                winner = None
                                if game.board.score[game.board.currentPlayer] > game.board.score[(game.board.currentPlayer + 1)%2]:
                                    winner = game.board.currentPlayer
                                    end = QMessageBox.information(game, "End", f"{game.panel.playersName[game.board.currentPlayer]} Win")
                                elif game.board.score[game.board.currentPlayer] == game.board.score[(game.board.currentPlayer + 1)%2]:
                                    winner = 2
                                    end = QMessageBox.information(game, "End", "No winner. Barrier case.")
                                else:
                                    winner = (game.board.currentPlayer + 1)%2
                                    end = QMessageBox.information(game, "End", f"{game.panel.playersName[(game.board.currentPlayer + 1)%2]} Win")
                                score = game.board.score
                                game.trace.winner = winner
                                game.trace.add_action(game.board.currentPlayer, (tempOrigin, (x,y)), self.step, game.board.getListBoard(), score)
                                game.board.setDefaultColors()
                                game.saveGame()
                                game.gameOneGoing = False
                            else:
                                if self.isStuck((self.color[((game.board.currentPlayer) + 1)%2 ])):
                                    game.setStatusTip("Player is stuck")
                                else:
                                    game.board.currentPlayer = (game.board.currentPlayer + 1)%2
                                    game.panel.updateCurrentPlayer()
                            game.board.setDefaultColors()




                elif game.board.currentPlayer == 1:
                    if(self.canPlayHere(x, y)):
                        print(self.isStuck((self.color[game.board.currentPlayer])), self.color[game.board.currentPlayer])
                        game.board.setDefaultColors()
                        # game.board.squares[x][y].setBackgroundColor("blue")
                        moves = self.getRealsMoves(x, y)
                        print("Actual move",(x,y), "Possible Moves",moves, "Origin", self.origin)
                        if self.origin is not None and (x,y) in self.getRealsMoves(self.origin[0], self.origin[1]):
                            self.move(self.origin, (x,y), game.board.currentPlayer)
                            score = game.board.score
                            game.trace.add_action(game.board.currentPlayer, (self.origin, (x,y)), self.step, game.board.getListBoard(), score)
                            print(game.trace.get_actions()[-1])
                            tempOrigin = self.origin
                            self.origin = None
                            print("Here")
                            captured = self.hasCaptured(x, y, self.color[game.board.currentPlayer])
                            print(captured)
                            if(len(captured)>0):
                                self.no_win = 0
                                for pos in captured:
                                    game.board.squares[pos[0]][pos[1]].removePiece()
                                    game.board.score[game.board.currentPlayer] += 1
                            else:
                                self.no_win += 1
                            print("Joueur 1", game.board.score[game.board.currentPlayer])
                            game.panel.updateScore(game.board.score)

                            if self.checkForEnd():
                                winner = None
                                if game.board.score[game.board.currentPlayer] > game.board.score[(game.board.currentPlayer + 1)%2]:
                                    winner = game.board.currentPlayer
                                    end = QMessageBox.information(game, "End", f"{game.panel.playersName[game.board.currentPlayer]} Win")
                                elif game.board.score[game.board.currentPlayer] == game.board.score[(game.board.currentPlayer + 1)%2]:
                                    winner = 2
                                    end = QMessageBox.information(game, "End", "No winner. Barrier case.")
                                else:
                                    winner = (game.board.currentPlayer + 1)%2
                                    end = QMessageBox.information(game, "End", f"{game.panel.playersName[(game.board.currentPlayer + 1)%2]} Win")
                                score = game.board.score
                                game.trace.winner = winner
                                game.trace.add_action(game.board.currentPlayer, (tempOrigin, (x,y)), self.step, game.board.getListBoard(), score)
                                game.board.setDefaultColors()
                                game.saveGame()
                                game.gameOneGoing = False
                            else:
                                if self.isStuck((self.color[((game.board.currentPlayer) + 1)%2 ])):
                                    game.setStatusTip("Player is stuck")
                                else:
                                    game.board.currentPlayer = (game.board.currentPlayer + 1)%2
                                    game.panel.updateCurrentPlayer()
                            game.board.setDefaultColors()





    def move(self, origin, dest, currentPlayer):
        game.board.squares[origin[0]][origin[1]].removePiece()
        game.board.squares[dest[0]][dest[1]].setPiece(Piece(currentPlayer, self.color[currentPlayer]))

    def checkForEnd(self):
        #C'est con mais bon
        if not self.getPlayerPiece((game.board.currentPlayer + 1)%2) or len(self.getPlayerPiece((game.board.currentPlayer + 1)%2)) == 1:
            return True
        if self.no_win >= 50 :
            return True



class BoardSquare(QLabel, QWidget, QtCore.QObject):

    trigger = QtCore.pyqtSignal(int, int)
    def __init__(self, col, row, gameSize, parent = None):
        super(BoardSquare, self).__init__(parent)
        #Dimensions
        self.setMinimumSize(100, 100)
        self.setScaledContents(False)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.trigger.connect(GameWindow.coord)
        self.column = col
        self.row = row
        self.gameSize = gameSize

        #In Game
        self.piece = None
        self.active = False
        self.setStatusTip(self.toNotation())
        #SquareColor
        if col%2 == 0:
            if row%2 == 0:
                self.__setColor(1)
                self.backgroundColor = "grey"
            else:
                self.__setColor(0)
                self.backgroundColor = "white"
        else:
            if row%2 == 0:
                self.__setColor(0)
                self.backgroundColor = "white"
            else:
                self.__setColor(1)
                self.backgroundColor = "grey"

    def Active(self, active):
        self.active = active
        self.setStyleSheet('QLabel { background-color : ' + self.backgroundColor + '; }')


    def setActive(self, color):
        if(type(color)==str):
            self.active = True
            self.setStyleSheet('QLabel { background-color : ' + color + '; }')
        elif(type(color)==bool):
            self.active = color
            self.setStyleSheet('QLabel { background-color : ' + self.backgroundColor + '; }')


    def isPiece(self):
        if self.piece == None:
            return False
        return True

    def isActive(self):
        return self.active

    def getPiece(self):
        return self.piece

    def setPiece(self, piece):
        self.piece = piece
        self.setPixmap(piece.getImage())
        self.setStatusTip(self.toNotation() + " - " + self.piece.color)

    def removePiece(self):
        self.piece = None
        empty = QtGui.QPixmap(0, 0)
        self.setPixmap(empty)
        self.setStatusTip(self.toNotation())


    def __setColor(self, color):

        if color == 0:
            self.setStyleSheet("""QLabel { background-color : white; } """)
        elif color == 1:
            self.setStyleSheet("""QLabel { background-color : grey; } """)
        else:
            raise Exception("Incorrect chess square color")
        self.color = color

    def setBackgroundColor(self, color):
        self.backgroundColor = color
        self.setStyleSheet('QLabel { background-color : ' + color + '; }')

    def toNotation(self):
        coordinates = str()
        x = self.column
        y = self.row
        if self.column>=0 and self.column<self.gameSize and self.row>=0 and self.row<self.gameSize:
            coordinates += str(str(x) + " ")
            coordinates += str(str(y) + " ")
        return  coordinates

    def mousePressEvent(self, ev):
        if ev.button() == 1:
            if self.active == True and game.gameOneGoing == True:

                # self.setPiece(Piece(1, "black"))
                x=self.column
                y=self.row
                # game.rulesgame=RulesGame();
                # game.rulesgame.play(x,y)
                # game.rulesgame.Play(x,y);
                # game.board.squares[x][y].setPiece(Piece(1,"black")) #Voilà ici on peut recupere la board donc place au regle du jeu et une fonction play play
                # self.trigger.emit(self.row, self.column)




class GameWindow(QMainWindow):
    dethToCover = 9

    def __init__(self, gameSize, players, timeout=.50, sleep_time = .500, parent = None):
        super(GameWindow, self).__init__(parent)
        self.setWindowTitle("[*] MAIC 2018 - Seega Game")
        self.saved = True
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.statusBar()
        self.gameOneGoing = False
        self.setWindowIcon(QtGui.QIcon("pieces/icon.png"))
        layout = QHBoxLayout()
        layout.addStretch()

        # self.gameSize = gameSize

        # self.board = Board(gameSize)
        self.player1=players[0]
        self.player2=players[1]
        playersName = [player.getName() for player in players]
        self.board = Board(gameSize)
        self.trace = Trace(self.board.getListBoard(), playersName)
        self.rulesgame = RulesGame()
        # chessboard->generateChessPieces();
        # connect(chessboard,SIGNAL(checkMate(int)),this,SLOT(game_over(int)));
        # connect(chessboard,SIGNAL(nextMove()), this, SLOT(setNotSaved()));

        layout.addWidget(self.board)
        layout.addSpacing(15)

        self.panel = Panel(self.board, playersName)

        # connect(chessboard,SIGNAL(newLost()), panel, SLOT(updateLost()));
        # connect(chessboard,SIGNAL(nextMove()), panel, SLOT(updateCurrentPlayer()));

        layout.addWidget(self.panel)

        layout.addStretch()

        content = QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content)
        self.createMenu()


    def refresh(self):
        print("coucou")


    # @QtCore.pyqtSlot(int)
    # @QtCore.pyqtSlot('QString')
    @QtCore.pyqtSlot(int, QGraphicsObject)
    def coord(self):
        print("cc")
        # print(GameWindow.message)


    def createMenu(self):
        menu = self.menuBar()
        #Game Menu
        gameMenu = menu.addMenu("Game")

        #New Game Submenu
        newGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/New file.png")), 'New Game', self)
        newGameAction.setShortcut(QtGui.QKeySequence.New)
        newGameAction.setStatusTip("New game Luncher")
        newGameAction.triggered.connect(self.newGame)
        gameMenu.addAction(newGameAction)

        gameMenu.addSeparator()

        #Load Game Submenu
        loadGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Open file.png")), 'Load Game', self)
        loadGameAction.setShortcut(QtGui.QKeySequence.Open)
        loadGameAction.setStatusTip("Load a previous game")
        loadGameAction.triggered.connect(self.loadGame)
        gameMenu.addAction(loadGameAction)

        #Save Game
        saveGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Save.png")), 'Save Game', self)
        saveGameAction.setShortcut(QtGui.QKeySequence.Save)
        saveGameAction.setStatusTip("Save current game")
        saveGameAction.triggered.connect(self.saveGame)
        gameMenu.addAction(saveGameAction)

        #Load Game
        replayGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Save.png")), 'Replay Game', self)
        replayGameAction.setShortcut(QtGui.QKeySequence.Close)
        replayGameAction.setStatusTip("Replay ended game")
        replayGameAction.triggered.connect(self.replayGame)
        gameMenu.addAction(replayGameAction)

        gameMenu.addSeparator()

        #Exit and close game
        exitGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Close.png")), 'Exit Game', self)
        exitGameAction.setShortcut(QtGui.QKeySequence.Quit)
        exitGameAction.setMenuRole(QAction.QuitRole)
        exitGameAction.setStatusTip("Exit and close window")
        exitGameAction.triggered.connect(self.exitGame)
        gameMenu.addAction(exitGameAction)

        menu.addSeparator()

        #Help Menu
        helpMenu = menu.addMenu("Help")

        #Rules
        gameRulesAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Help.png")), 'Rules', self)
        gameRulesAction.setMenuRole(QAction.AboutRole)
        gameRulesAction.triggered.connect(self.gameRules)
        helpMenu.addAction(gameRulesAction)

        helpMenu.addSeparator()

        #About
        aboutAction = QAction( 'About', self)
        aboutAction.setMenuRole(QAction.AboutRole)
        aboutAction.triggered.connect(self.about)
        helpMenu.addAction(aboutAction)

    def newGame(self):
        newGame = QMessageBox.question(self, 'New Game', "You're about to start a new Game.", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if newGame == QMessageBox.Yes:
            self.board.resetBoard()
            game.board.score = [0, 0]
            self.gameOneGoing = True
            game.rulesgame = RulesGame()
            game.panel.updateScore([0, 0])
            self.board.activeAllSquares()
            self.board.setCurrentPlayer(0)
            self.panel.resetPanelPlayer()
            self.startBattle()
        else:
            pass




    def startBattle(self):
        i=0
        while self.gameOneGoing :
            app.processEvents()
            i = i+1
            time.sleep(0.1)
            if self.board.currentPlayer==0:
                board =self.board.getListBoard()
                print(board)
                if self.rulesgame.step==0:  #ici

                    (a,b)=self.player1.play(self.dethToCover, board, self.rulesgame.step)
                    self.rulesgame.play(a,b)
                    time.sleep(self.sleep_time)
                    app.processEvents()
                else:
                    print("here")
                    (a,b,c,d)=self.player1.play(self.dethToCover, board,self.rulesgame.step)
                    self.board.squares[a][b].setBackgroundColor("blue")
                    self.board.squares[c][d].setBackgroundColor("green")
                    app.processEvents()
                    self.rulesgame.play(a,b)
                    self.board.squares[a][b].setBackgroundColor("blue")
                    self.board.squares[c][d].setBackgroundColor("green")
                    app.processEvents()
                    time.sleep(self.sleep_time)
                    app.processEvents()
                    self.rulesgame.play(c,d)
                    time.sleep(self.sleep_time)
                    app.processEvents()


            elif(self.board.currentPlayer==1):
                board = self.board.getListBoard()
                if(self.rulesgame.step==0):
                    (a,b)=self.player2.play(self.dethToCover, board, self.rulesgame.step)
                    self.rulesgame.play(a,b)
                    time.sleep(self.sleep_time)
                    app.processEvents()
                else:
                    print("here2")
                    (a,b,c,d)= self.player2.play(self.dethToCover, board, self.rulesgame.step)
                    self.board.squares[a][b].setBackgroundColor("blue")
                    self.board.squares[c][d].setBackgroundColor("green")
                    app.processEvents()
                    game.rulesgame.play(a,b)
                    self.board.squares[a][b].setBackgroundColor("blue")
                    self.board.squares[c][d].setBackgroundColor("green")
                    app.processEvents()
                    time.sleep(self.sleep_time)
                    app.processEvents()
                    game.rulesgame.play(c,d)
                    time.sleep(self.sleep_time)
                    app.processEvents()
            game.board.setDefaultColors()
        game.board.setDefaultColors()




    def loadGame(self):
        name =QtWidgets.QFileDialog.getOpenFileName(self, 'Load Game')
        listBoard = None
        if name[0] != "":
            listBoard = self.trace.load_trace(name[0])
            if listBoard.winner != -1:
                print(listBoard.winner)
                warning = QMessageBox.warning(self, "Game Ended", "This game is already finished")
            else:
                if not listBoard.get_actions():
                    self.trace = listBoard
                else:
                    self.gameOneGoing = True
                    self.board.resetBoard()
                    self.rulesgame = RulesGame()
                    self.board.putListBoard(listBoard.get_last_board()[3])
                    self.panel.setName(listBoard.names)
                    self.trace = listBoard
                    self.board.currentPlayer = (listBoard.get_last_board()[0] + 1)%2
                    self.rulesgame.step = listBoard.get_last_board()[2]
                    self.panel.updateCurrentPlayer()
                    self.board.score = listBoard.score
                    self.panel.updateScore(self.board.score)
                    self.board.activeAllSquares()
        else:
            pass

    def saveGame(self):
        if self.gameOneGoing:
            name =QtWidgets.QFileDialog.getSaveFileName(self, 'Save Game')
            self.trace.write(name[0])
        else:
            warning = QMessageBox.warning(self, "Warning", "No game ongoing")

    def replayGame(self):
        name =QtWidgets.QFileDialog.getOpenFileName(self, 'Load Game')
        listBoard = None
        i = -1
        if name[0] != "":
            listBoard = self.trace.load_trace(name[0])
            if listBoard.winner == -1:
                warning = QMessageBox.warning(self, "Game Not ended", "This game is not yet finished. Load it to finish it")
            else:
                self.board.resetBoard()
                # print("Ok")
                self.rulesgame = RulesGame()
                self.panel.setName(listBoard.names)
                self.panel.updateScore([0,0])
                actions = listBoard.get_actions()
                print(actions)
                # print(len(actions))
                # game.board.putListBoard(actions[1][3])
                # time.sleep(1)
                # game.board.putListBoard(actions[2][3])

                for action in actions:
                    i+=1
                    app.processEvents()
                    if action[2] == 0:
                        # print(i, action[3], action[0])
                        # print("ok")
                        game.board.currentPlayer = action[0]
                        game.panel.updateCurrentPlayer()
                        game.board.putListBoard(action[3])
                        time.sleep(self.sleep_time)
                    elif action[2] == 1:
                        game.panel.updateScore(action[4])
                        game.board.score = action[4]
                        print(game.board.score)
                        game.board.currentPlayer = action[0]
                        game.panel.updateCurrentPlayer()
                        game.board.putListBoard(actions[i-1][3])
                        origin, end = action[1]
                        game.board.squares[origin[0]][origin[1]].setBackgroundColor("blue")
                        time.sleep(self.sleep_time)
                        app.processEvents()
                        game.board.squares[end[0]][end[1]].setBackgroundColor("green")
                        time.sleep(self.sleep_time)
                        app.processEvents()
                        time.sleep(self.sleep_time)
                        game.rulesgame.move(origin, end, game.board.currentPlayer)
                        game.board.putListBoard(action[3])
                        time.sleep(self.sleep_time)
                        game.panel.updateScore(game.board.score)
                        app.processEvents()
                        game.board.setDefaultColors()
                end = QMessageBox.information(game, "End", f" {game.panel.playersName[game.board.currentPlayer]} Win")












    def exitGame(self):
        return True

    def gameRules(self):
        rules = "Seega Rules"
        box = QMessageBox()
        box.about(self, "Rules", rules)

    def about(self):
        about = "MAIC 2018 Seega Game by MIFY"
        box = QMessageBox()
        box.about(self, "About", about)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.exitGame() == True:
            a0.accept()
        else:
            a0.ignore()








class Board(QWidget):
    def __init__(self, gameSize, parent = None):
        super(Board, self).__init__(parent)
        self.currentPlayer = 0
        self.color = ["black", "white"]
        self.gameSize = gameSize
        self.score = [0, 0]
        self.setFixedSize(100 * gameSize, 100 * gameSize)
        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)
        self.blackColor = "brown"
        # self.blackColor = "#413B46"
        self.whiteColor = "#E0EEF1"
        self.selectColor = "blue"
        self.attackColor = "red"
        self.squares = list()
        for i in range(gameSize):
            tempList = list()
            for j in range(gameSize):
                square =  BoardSquare(i, j, gameSize)
                gridLayout.addWidget(square, gameSize-i, j)
                # connect(chesssquares[i][j],SIGNAL(clicked(int,int)),this,SLOT(validateClick(int,int)));
                tempList.append(square)
            self.squares.append(tempList)
        self.setDefaultColors()
        self.setLayout(gridLayout)

    def setDefaultColors(self):
        for i in range(self.gameSize):
            for j in range(self.gameSize):
                if i%2 == 0:
                    if j%2 == 0:
                        self.squares[i][j].setBackgroundColor(self.blackColor)
                    else:
                        self.squares[i][j].setBackgroundColor(self.whiteColor)
                else:
                    if j%2 == 0:
                        self.squares[i][j].setBackgroundColor(self.whiteColor)
                    else:
                        self.squares[i][j].setBackgroundColor(self.blackColor)


    def dealWIthCord(self, x, y):
        print("ok")

    def setCurrentPlayer(self, player):
        self.currentPlayer = player

    def resetBoard(self):
        for i in range(self.gameSize):
            for j in range(self.gameSize):
                self.squares[i][j].removePiece()

    def activeAllSquares(self):
        for i in range(self.gameSize):
            for j in range(self.gameSize):
                self.squares[i][j].setActive(True)

    def desactiveAllSquares(self):
        for i in range(self.gameSize):
            for j in range(self.gameSize):
                self.squares[i][j].setActive(False)

    def getListBoard(self):
        list_board = []
        for i in range(self.gameSize):
            temp = []
            for j in range (self.gameSize):
                if not self.squares[i][j].isPiece():
                    temp.append(None)
                else:
                    temp.append(self.squares[i][j].piece.getColor())
            list_board.append(temp)
        return list_board

    def putListBoard(self, listBord):
        for i in range(self.gameSize):
            for j in range(self.gameSize):
                if listBord[i][j] == None:
                    self.squares[i][j].removePiece()
                elif listBord[i][j] == "black":
                    self.squares[i][j].setPiece(Piece(0, "black"))
                elif listBord[i][j] == "white":
                    self.squares[i][j].setPiece(Piece(1, "white"))




    def dealWIthCord(self, x, y):
        print("ok")






if __name__== "__main__":
    import sys
    import ctypes
    myappid = 'myfi.maic.seega.1.0'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass
    app = QApplication(sys.argv)
    gameSize=5
    player1=IA(0, gameSize)
    player2=IA(1, gameSize)
    game = GameWindow(gameSize, [player1, player2])
    # game.board.squares[2][2].setActive("red")

    game.show()

    sys.exit(app.exec_())
