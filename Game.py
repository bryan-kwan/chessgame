
class Game():
    def __init__(self, board):
        self.board = board
        self.history = []
        self.turn = 'w' #which colour's turn it is
        self.pieces = [] #list of all pieces to keep track of what has been captured

    def move_piece(self, src_row, src_col, dest_row, dest_col): #moves a piece from src coordinates to dest coordinates
        if(self.check_legal_move(src_row, src_col, dest_row, dest_col)==False): #check if the move is legal
            return
        old_board = self.board.copy() #make a copy of the board state
        self.history.append(old_board) #store in history
        self.board.grid[dest_row][dest_col] = self.board.grid[src_row][src_col].copy() #copy piece from src to dest
        self.board.grid[src_row][src_col].colour = '' #src piece becomes empty
        self.board.grid[src_row][src_col].type = ''
        self.board.grid[dest_row][dest_col].first_move = False #the piece has moved now
        if self.turn=='w': #passes turns between players
            self.turn='b'
        else:
            self.turn='w'


    def check_legal_move(self, src_row, src_col, dest_row, dest_col): #checks if a move is allowed in standard chess

        src_square = self.board.grid[src_row][src_col]
        dest_square = self.board.grid[dest_row][dest_col]
        your_colour = src_square.colour
        if your_colour=='w':
            opposite_colour='b'
        else:
            opposite_colour='w'
        #general rules-------------------------------------

        #empty squares can't move
        if(src_square.type==''):
            return False 
        #it has to be your turn to move
        if(self.turn=='w' and your_colour=='b'):
            return False
        if(self.turn=='b' and your_colour=='w'):
            return False
        #you can't capture your own pieces    
        if(src_square.colour==dest_square.colour): 
            return False 
        #can't put your own king in check
        #look at the board state of the candidate move
        next_board = self.board.copy()
        for row in next_board.grid: #find your king
            for element in row:
                if element.type=='k' and element.colour==your_colour:
                    king = element
        next_board.grid[dest_row][dest_col] = self.board.grid[src_row][src_col].copy()
        next_board.grid[src_row][src_col].type=''
        next_board.grid[src_row][src_col].colour=''
        next_board.grid[dest_row][dest_col].first_move = False
        if(self.check_square_attacked(king.row, king.col, your_colour, next_board)==True): #check if your move makes your king get attacked
            return False
        #general rules-------------------------------------

        #pawn rules------------------------------------
        if(src_square.type=='p'): 
            if(src_square.first_move==True):
                movable_squares = 2
            else:
                movable_squares = 1
            if(dest_row>src_row and src_square.colour=='w'): #pawns can't move backwards ever
                return False
            if(dest_row<src_row and src_square.colour=='b'): #pawns can't move backwards ever
                return False
            if(dest_col!=src_col and dest_row==src_row): #pawns can't move sideways ever
                return False
            elif(abs(dest_row-src_row)>movable_squares): #pawns can only move 1 or 2 spaces
                return False
            elif(dest_col==src_col):
                if(dest_square.type!=''): #pawns can't move forward into other pieces
                    return False
            elif(dest_col!=src_col and abs(dest_col-src_col)==1): #pawns can only move diagonally if they capture or en passant
                if(src_square.colour=='w' and dest_square.colour=='b'):
                    return True
                if(src_square.colour=='b' and dest_square.colour=='w'):
                    return True

                #en passant checker
                if src_square.colour=='w' and src_row==3: #white pawns can only en passant from the fifth rank
                    
                    last_board = self.history[len(self.history)-2]
                    last_square = last_board.grid[src_row-2][src_col-1]  #square enemy pawn was last on    
                    current_square = self.board.grid[src_row][src_col-1] #square enemy pawn is currently on     
                    if (src_col != 0 and last_square.type=='p'  #checks for pawns to the left
                    and last_square.colour=='b' 
                    and last_square.first_move==True):
                        if(current_square.type=='p' and current_square.colour=='b'):
                            self.en_passant(src_row, src_col, dest_row, dest_col)
                            return True
                    last_square = last_board.grid[src_row-2][src_col+1] #redefined for pawn on the right
                    current_square = self.board.grid[src_row][src_col+1]
                    if (src_col!=7 and last_square.type=='p' #checks for pawns to the right
                    and last_square.colour=='b'
                    and last_square.first_move==True):
                        if(current_square.type=='p' and current_square.colour=='b'):
                            self.en_passant(src_row, src_col, dest_row, dest_col)
                            return True
                if src_square.colour=='b' and src_row==4: #black pawns can only en passant from the fourth rank
                    last_board = self.history[len(self.history)-2]
                    last_square = last_board.grid[src_row+2][src_col-1]  #square enemy pawn was last on    
                    current_square = self.board.grid[src_row][src_col-1] #square enemy pawn is currently on 
                    if (src_col != 0 and last_square.type=='p'  #checks for pawns to the right
                    and last_square.colour=='b' 
                    and last_square.first_move==True):
                        if(current_square.type=='p' and current_square.colour=='b'):
                            self.en_passant(src_row, src_col, dest_row, dest_col)
                            return True
                    last_square = last_board.grid[src_row+2][src_col+1]  #square enemy pawn was last on    
                    current_square = self.board.grid[src_row][src_col+1] #square enemy pawn is currently on 
                    if (src_col!=7 and last_square.type=='p' #checks for pawns to the left
                    and last_square.colour=='b'
                    and last_square.first_move==True):
                        if(current_square.type=='p' and current_square.colour=='b'):
                            self.en_passant(src_row, src_col, dest_row, dest_col)
                            return True
                return False
        #pawn rules----------------------------------------
        
        #rook moves----------------------------------------
        if(src_square.type=='r'):
            if(dest_row!=src_row and dest_col!=src_col): #rooks can't move diagonally
                return False
            if(dest_row==src_row): #when rooks move sideways
                if dest_col > src_col:
                    low_col = src_col
                    hi_col = dest_col
                else:
                    low_col = dest_col
                    hi_col = src_col
                for i in range(low_col+1, hi_col): #can't move through other pieces
                    square = self.board.grid[src_row][i]
                    if(square.type!=''): 
                        return False
            if(dest_col==src_col): #when rooks move vertically
                if dest_row > src_row:
                    low_row = src_row
                    hi_row = dest_row
                else:
                    low_row = dest_row
                    hi_row = src_row
                for i in range(low_row+1, hi_row): #can't move through other pieces
                    square = self.board.grid[i][src_col]
                    if square.type!='':
                        return False

        #rook moves----------------------------------------

        #knight moves--------------------------------------
        if(src_square.type=='n'):
            if(abs(dest_row-src_row)!=2 and abs(dest_col-src_col)!=2): #knights move two along a row or column then one along the other row or column
                return False
            if(abs(dest_row-src_row)==2): #if we move two rows, we must move one column
                if(abs(dest_col-src_col)!=1):
                    return False
            if(abs(dest_col-src_col)==2): #if we move two columns, we must move one row
                if(abs(dest_row-src_row)!=1):
                    return False
        #knight moves--------------------------------------

        #bishop moves--------------------------------------
        if(src_square.type=='b'):
            
            if(abs(dest_row-src_row)!=abs(dest_col-src_col)): #bishops move diagonally (ie. horizontal = vertical movement)
                return False
            #can't move through other pieces
            if dest_row > src_row and dest_col > src_col: #bottom right check
                for i in range(1, abs(dest_row-src_row)):
                    if self.board.grid[src_row+i][src_col+i].type!='':
                        return False
            if dest_row > src_row and dest_col < src_col: #bottom left
                for i in range(1, abs(dest_row-src_row)):
                    if self.board.grid[src_row+i][src_col-i].type!='':
                        return False
            if dest_row < src_row and dest_col > src_col: #top right
                for i in range(1, abs(dest_row-src_row)):
                    if self.board.grid[src_row-i][src_col+i].type!='':
                        return False
            if dest_row < src_row and dest_col < src_col: #top left
                for i in range(1, abs(dest_row-src_row)):
                    if self.board.grid[src_row-i][src_col-i].type!='':
                        return False

        #bishop moves--------------------------------------

        #queen moves--------------------------------------
        if(src_square.type=='q'): #has movement of rook + bishop
            if(dest_row!=src_row and dest_col!=src_col and abs(dest_col-src_col)!=abs(dest_row-src_row)):
                return False      
            #can't move through other pieces
            #check horizontal and vertical
            if(dest_row==src_row): #when queen moves sideways
                if dest_col > src_col:
                    low_col = src_col
                    hi_col = dest_col
                else:
                    low_col = dest_col
                    hi_col = src_col
                for i in range(low_col+1, hi_col): #can't move through other pieces
                    square = self.board.grid[src_row][i]
                    if(square.type!=''): 
                        return False
            if(dest_col==src_col): #when queen moves vertically
                if dest_row > src_row:
                    low_row = src_row
                    hi_row = dest_row
                else:
                    low_row = dest_row
                    hi_row = src_row
                for i in range(low_row+1, hi_row): #can't move through other pieces
                    square = self.board.grid[i][src_col]
                    if square.type!='':
                        return False
            #check diagonal
            if dest_row > src_row and dest_col > src_col: #bottom right check
                for i in range(1, abs(dest_row-src_row)):
                    if self.board.grid[src_row+i][src_col+i].type!='':
                        return False
            if dest_row > src_row and dest_col < src_col: #bottom left
                for i in range(1, abs(dest_row-src_row)):
                    if self.board.grid[src_row+i][src_col-i].type!='':
                        return False
            if dest_row < src_row and dest_col > src_col: #top right
                for i in range(1, abs(dest_row-src_row)):
                    if self.board.grid[src_row-i][src_col+i].type!='':
                        return False
            if dest_row < src_row and dest_col < src_col: #top left
                for i in range(1, abs(dest_row-src_row)):
                    if self.board.grid[src_row-i][src_col-i].type!='':
                        return False            
        #queen moves--------------------------------------

        #king moves--------------------------------------
        if src_square.type=='k':
            if src_square.first_move==True: #castling
                if(dest_row==src_row):
                    if(dest_col==6 and self.board.grid[src_row][7].type=='r' and self.board.grid[src_row][7].first_move==True): #king side castle
                        if(src_square.colour=='w'):
                            if(self.check_square_attacked(src_row, 5, 'w', self.board)==False):
                                self.castle_kingside('w')
                                return True
                        elif(self.check_square_attacked(src_row, 5, 'b', self.board)==False):
                            self.castle_kingside('b')
                            return True
                    if(dest_col==2 and self.board.grid[src_row][0].type=='r' and self.board.grid[src_row][0].first_move==True): #queen side castle
                        if(src_square.colour=='w'):
                            if(self.check_square_attacked(src_row, 3, 'w', self.board)==False):
                                self.castle_queenside('w')
                                return True
                        elif(self.check_square_attacked(src_row, 3, 'b', self.board)==False):
                            self.castle_queenside('b')
                            return True
            if abs(dest_row-src_row)>1 or abs(dest_col-src_col)>1: #king can only move 1 square in any direction
                return False

        #king moves--------------------------------------
        return True

    def check_square_attacked(self, row, col, colour, board): #checks if a square is being attacked (ie. can be captured next turn) for a given colour
        your_colour = colour
        if your_colour=='w':
            opposite_colour='b'
        else:
            opposite_colour='w'
        r = row-1
        while r >= 0: #checks above
            square = board.grid[r][col]
            if square.colour==your_colour: #can't be attacked through your own pieces
                break
            if square.type=='p': #pawns can never attack vertically
                break
            if square.type=='k': #knights can never attack vertically
                break
            if square.type=='b': #bishops don't attack vertically
                break
            if square.type=='r': #black rook attacking
                return True
            if square.type=='q': #black queen
                return True
            r+=-1
        r = row+1
        while r <= 7: #checks below
            square = board.grid[r][col]
            if square.colour==your_colour: #can't be attacked through your own pieces
                break
            if square.type=='p': #pawns can never attack vertically
                break
            if square.type=='k': #knights can never attack vertically
                break
            if square.type=='b': #bishops don't attack vertically
                break
            if square.type=='r': #black rook attacking
                return True
            if square.type=='q': #black queen
                return True
            r+=1
        r = row-1
        offset = 1
        while r >=0 and (col+offset<=7): #checks top right diagonal
            square = board.grid[r][col+offset]
            if square.colour==your_colour: #can't be attacked through your own pieces
                break
            if square.type=='p' and offset==1: #attacking black pawn
                return True
            if square.type=='k': #knights can never attack diagonally
                break
            if square.type=='b': #attacking black bishop
                return True
            if square.type=='r': #rooks never attack diagonally
                break
            if square.type=='q': #attacking black queen
                return True
            r+=-1    
            offset+=1   
        r = row-1
        offset = 1
        while r >=0 and (col-offset>=0): #checks top left diagonal
            square = board.grid[r][col-offset]
            if square.colour==your_colour: #can't be attacked through your own pieces
                break
            if square.type=='p' and offset==1: #attacking black pawn
                return True
            if square.type=='k': #knights can never attack diagonally
                break
            if square.type=='b': #attacking black bishop
                return True
            if square.type=='r': #rooks never attack diagonally
                break
            if square.type=='q': #attacking black queen
                return True
            r+=-1   
            offset+=1                                             
        c = col-1
        while c>=0: #checks left
            square = board.grid[row][c]
            if square.colour==your_colour: #can't be attacked through your own pieces
                break
            if square.type=='p': #pawns can never attack horizontally
                break
            if square.type=='k': #knights can never attack horizontally
                break
            if square.type=='b': #bishops don't attack horizontally
                break
            if square.type=='r': #black rook attacking
                return True
            if square.type=='q': #black queen
                return True
            c+=-1
        c = col+1
        while c<=7: #checks right
            square = board.grid[row][c]
            if square.colour==your_colour: #can't be attacked through your own pieces
                break
            if square.type=='p': #pawns can never attack horizontally
                break
            if square.type=='k': #knights can never attack horizontally
                break
            if square.type=='b': #bishops don't attack horizontally
                break
            if square.type=='r': #black rook attacking
                return True
            if square.type=='q': #black queen
                return True
            c+=1                                        
        r = row+1
        offset = 1
        while r <=7 and (col-offset>=0): #checks bot left diagonal
            square = board.grid[r][col-offset]
            if square.colour==your_colour: #can't be attacked through your own pieces
                break
            if square.type=='p': #can't be attacked from behind by a pawn
                break
            if square.type=='k': #knights can never attack diagonally
                break
            if square.type=='b': #attacking black bishop
                return True
            if square.type=='r': #rooks never attack diagonally
                break
            if square.type=='q': #attacking black queen
                return True
            r+=1
            offset+=1
        r = row+1
        offset = 1
        while r <=7 and (col+offset>=0): #checks bot right diagonal
            square = board.grid[r][col+offset]
            if square.colour==your_colour: #can't be attacked through your own pieces
                break
            if square.type=='p': #can't be attacked from behind by a pawn
                break
            if square.type=='k': #knights can never attack diagonally
                break
            if square.type=='b': #attacking black bishop
                return True
            if square.type=='r': #rooks never attack diagonally
                break
            if square.type=='q': #attacking black queen
                return True
            r+=-1
            offset+=1
        #brute force checking for knight moves
        if row-2>=0:
            if col-1>=0:
                square = board.grid[row-2][col-1] #2 top 1 left
                if square.type=='n' and square.colour==opposite_colour:
                    return True
            if col+1<=7:
                square = board.grid[row-2][col+1] #2 top 1 right
                if square.type=='n' and square.colour==opposite_colour:
                    return True
        if row+2<=7:
            if col-1>=0:
                square = board.grid[row+2][col-1] #2 bot 1 left
                if square.type=='n' and square.colour==opposite_colour:
                    return True
            if col+1<=7:
                square = board.grid[row+2][col+1] #2 bot 1 right
                if square.type=='n' and square.colour==opposite_colour:
                    return True
        if row-1>=0:
            if col-2>=0:
                square = board.grid[row-1][col-2] #1 top 2 left
                if square.type=='n' and square.colour==opposite_colour:
                    return True
            if col+2<=7:
                square = board.grid[row-1][col+2] #1 top 2 right
                if square.type=='n' and square.colour==opposite_colour:
                    return True
        if row+1<=7:
            if col-2>=0:
                square = board.grid[row+1][col-2] #1 bot 2 left
                if square.type=='n' and square.colour==opposite_colour:
                    return True
            if col+2<=7:
                square = board.grid[row+1][col+2] #1 bot 2 right
                if square.type=='n' and square.colour==opposite_colour:
                    return True
            
        return False #not attacked
        
    def promote_pawn(self, src_row, src_col, dest_row, dest_col): #checks if a pawn is promoted and if so it converts to a queen
        print("you promoted!")
    
    #the move_piece function already moves the king so to complete castling we must move the rook as well
    def castle_kingside(self, colour):
        print("castled kingside")

    def castle_queenside(self, colour):
        print("castled queenside")
    
    #the move_piece function already moves the attacking pawn so to en passant we need to capture the enemy pawn (located behind the attacking pawn)
    def en_passant(self, src_row, src_col, dest_row, dest_col):
        print("en passant!")

    def check_checkmate(self, colour): #checks if one side's king has no more legal moves and is currently attacked
        pass