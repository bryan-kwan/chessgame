import pygame
import Piece


class Board:
    def __init__(self):
        self.grid = [ [None]*8 for i in range(8)]
        for x in range(len(self.grid)): #cols
            for y in range(len(self.grid)): #rows, set each grid tile to be a Piece object
                self.grid[x][y] = Piece.Piece('','','', x, y) #empty tile
        self.background_colour = (0, 0, 0) 
        self.border_colour = (255, 255, 255)
        self.dark_colour = (118, 150, 86) #colour of dark squares
        self.light_colour = (238, 238, 210) #colour of light squares
    
    def copy(self): #creates a deep copy of the Board object
        new_board = Board()
        for x in range(8):
            for y in range(8):
                new_board.grid[x][y] = self.grid[x][y].copy(x, y)
        return new_board

    def draw(self, surface, grid_size): #creates a grid of squares and renders pieces
        self.squareSize = grid_size/8 
        for y in range(len(self.grid)): #rows
            for x in range(len(self.grid)): #columns
                square = self.grid[y][x]
                rect = pygame.Rect(x*self.squareSize, y*self.squareSize, self.squareSize, self.squareSize)
                if (x+y) % 2 == 0: #light colour squares
                    square.rect = pygame.draw.rect(surface, self.light_colour, rect)
                    self.draw_pieces(square, surface)
                else: #dark colour squares
                    square.rect = pygame.draw.rect(surface, self.dark_colour, rect)
                    self.draw_pieces(square, surface)
                    
    def setup_pieces(self): #default chess piece setup
        for y in range(len(self.grid)): #rows
            for x in range(len(self.grid)): #columns
                if(x==0): #top two rows are black
                    self.grid[x][y].colour = 'b' 
                    if(y==0 or y==7): #rooks
                        self.grid[x][y].type = 'r'
                    if(y==1 or y==6): #knights
                        self.grid[x][y].type = 'n'
                    if(y==2 or y==5): #bishops
                        self.grid[x][y].type = 'b'
                    if(y==3): #queen
                        self.grid[x][y].type = 'q'
                    if(y==4): #king
                        self.grid[x][y].type = 'k'
                if(x==1): #black pawns
                    self.grid[x][y].colour = 'b'
                    self.grid[x][y].type = 'p'

                if(x==7): #bottom two rows are white
                    self.grid[x][y].colour = 'w' 
                    if(y==0 or y==7): #rooks
                        self.grid[x][y].type = 'r' 
                    if(y==1 or y==6): #knights
                        self.grid[x][y].type = 'n'
                    if(y==2 or y==5): #bishops
                        self.grid[x][y].type = 'b'
                    if(y==3): #queen
                        self.grid[x][y].type = 'q'
                    if(y==4): #king
                        self.grid[x][y].type = 'k'
                if(x==6): #white pawns
                    self.grid[x][y].colour = 'w'
                    self.grid[x][y].type = 'p'


    def draw_pieces(self, square, surface): #renders images of pieces
        if(square.colour=='b'): #renders black pieces
            if(square.type=='r'): #rooks
                square.img = pygame.image.load("images/b_rook.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='n'): #knights
                square.img = pygame.image.load("images/b_knight.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='b'): #bishops
                square.img = pygame.image.load("images/b_bishop.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='p'): #pawns
                square.img = pygame.image.load("images/b_pawn.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='q'): #queen
                square.img = pygame.image.load("images/b_queen.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='k'): #king
                square.img = pygame.image.load("images/b_king.png").convert_alpha()
                surface.blit(square.img, square.rect)
        if(square.colour=='w'): #renders white pieces
            if(square.type=='r'): #rooks
                square.img = pygame.image.load("images/w_rook.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='n'): #knights
                square.img = pygame.image.load("images/w_knight.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='b'): #bishops
                square.img = pygame.image.load("images/w_bishop.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='p'): #pawns
                square.img = pygame.image.load("images/w_pawn.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='q'): #queen
                square.img = pygame.image.load("images/w_queen.png").convert_alpha()
                surface.blit(square.img, square.rect)
            if(square.type=='k'): #king
                square.img = pygame.image.load("images/w_king.png").convert_alpha()
                surface.blit(square.img, square.rect)
