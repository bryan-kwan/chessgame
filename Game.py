import copy

class Game():
    def __init__(self, board):
        self.board = board
        self.history = []

    def move_piece(self, src_row, src_col, dest_row, dest_col): #moves a piece from src coordinates to dest coordinates
        self.new_board = self.board
        self.new_board.grid[dest_row][dest_col] = self.new_board.grid[src_row][src_col].copy() #copy piece from src to dest
        self.new_board.grid[src_row][src_col].colour = '' #delete piece from src
        self.new_board.grid[src_row][src_col].type = ''
        self.history.append(self.new_board) #store board state in history
                
