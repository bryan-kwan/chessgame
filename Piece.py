import pygame

class Piece:
    def __init__(self, colour, type, img, row, col): #each piece has a colour (its team), type (king, rook, etc.), an image file, a Rect object (to draw images), and coordinates
        self.colour = colour
        self.type = type
        self.img = img
        self.row = row 
        self.col = col
        self.rect = pygame.Rect #pygame coordinates
        self.captured = False #has the piece been captured
        self.first_move = True #has the piece moved yet

    def copy(self, row, col):
        new_piece = Piece(self.colour, self.type, self.img, row, col)
        new_piece.rect = self.rect
        return new_piece