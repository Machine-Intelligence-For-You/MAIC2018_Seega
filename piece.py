# Created by HaroldKS at 21/08/2018
from PyQt5 import QtGui

class Piece:
    def __init__(self, player_number, color):
        self.moveNumber = 0
        self.color = color
        self.player =  player_number

        if color == "white":
            self.image_url = "pieces/white_piece.png"
        else:
            self.image_url = "pieces/black_piece.png"

    def getImage(self):
        return QtGui.QPixmap(self.image_url)

    def getColor(self):
        return self.color

    def getPlayer(self):
        return self.player

    def getMoveNumber(self):
        return self.moveNumber

    def nextMove(self):
        self.moveNumber += 1