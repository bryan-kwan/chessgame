import pygame
import sys
import Board
import Game
import math

SQUARE_SIZE = 60
GRID_SIZE = SQUARE_SIZE*8 #images are 60 pixels
SCREEN_WIDTH = GRID_SIZE
SCREEN_HEIGHT = GRID_SIZE


def main():
    #setup
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test")
    game = Game.Game(Board.Board())
    board = game.board
    board.setup_pieces()
    surface.fill(board.background_colour)
    #main loop
    while True:
        for event in pygame.event.get(): #quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type ==pygame.MOUSEBUTTONDOWN: #checks for players dragging pieces
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    src_row = math.floor(mouse_y / SQUARE_SIZE)
                    src_col = math.floor(mouse_x / SQUARE_SIZE)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    dest_row = math.floor(mouse_y / SQUARE_SIZE)
                    dest_col = math.floor(mouse_x / SQUARE_SIZE)
                    game.move_piece(src_row, src_col, dest_row, dest_col)        
        board.draw(surface, GRID_SIZE) #draws board
        pygame.display.update()
    

if __name__ == "__main__":
    main()

