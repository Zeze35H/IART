import copy

WHITE_HB = 0 # white player homeboard (cima); has one black board and one white board
BLACK_HB = 1 # black player homeboard (baixo); has one black board and one white board
BLACK_BOARD = 0 # black colored boards (left side boards)
WHITE_BOARD = 1 # white colored boards (right side boards)

class Board:
    def __init__(self):
        self.boards = [[[['W','W','W','W'],
                         [' ',' ',' ',' '],
                         [' ',' ',' ',' '],
                         ['B','B','B','B']], 
                        
                        [['W','W','W','W'],
                         [' ',' ',' ',' '],
                         [' ',' ',' ',' '],
                         ['B','B','B','B']]],
                       
                       [[['W','W','W','W'],
                         [' ',' ',' ',' '],
                         [' ',' ',' ',' '],
                         ['B','B','B','B']], 
                        
                        [['W','W','W','W'],
                         [' ',' ',' ',' '],
                         [' ',' ',' ',' '],
                         ['B','B','B','B']]]] 
        
    def displayHomeboard(self, color, color_string, row_number):
        
        
        print("   _______________________  |  _______________________ ")
        
        for row in range(4):
            print("  |     |     |     |     | | |     |     |     |     |")
            print(row_number, end=" ") # row label
            
            for black_cell in range(4): # print row from black board
                print("|  " + self.boards[color][BLACK_BOARD][row][black_cell] + "  ", end="")
            print("| | ", end="")
            for white_cell in range(4): # print row from white board
                print("|  " + self.boards[color][WHITE_BOARD][row][white_cell] + "  ", end="")
                
            print("|\n  |_____|_____|_____|_____| | |_____|_____|_____|_____|", end="")
            if(row == 1):
                print("   " + color_string + "'s Homeboards", end="")
            print("")
            
            row_number += 1
    
    
    def display(self):
        print("\n         Black Boards               White Boards      ")
        print("\n     A     B     C     D    |    E     F     G     H")
        self.displayHomeboard(WHITE_HB, "White", 1)
        print(" ___________________________|__________________________")
        self.displayHomeboard(BLACK_HB, "Black", 5)
        

class GameLogic:
    def __init__(self):
        self.board = Board()
        self.player = 1 # white=0, black=1

    # =============================================================================
    #  AUX FUNTIONS
    # =============================================================================
    
    def switch_01(self, number):
        return number + 1 % 2
    
    def parseInt(self, x):
        try:
            int_x = int(x)
            return int_x
        except ValueError:
            return None
        
    def parseInput(self, row, col):

        int_row = self.parseInt(row) 
        if(int_row is None or int_row < 1 or int_row > 8):
            return None, None, None
        row_index = (int_row - 1) % 4
            
        if(col == 'A' or col == 'a'):
            return BLACK_BOARD, row_index, 0
        elif(col == 'B' or col == 'b'):
            return BLACK_BOARD, row_index, 1
        elif(col == 'C' or col == 'c'):
            return BLACK_BOARD, row_index, 2
        elif(col == 'D' or col == 'd'):
            return BLACK_BOARD, row_index, 3
        
        elif(col == 'E' or col == 'e'):
            return WHITE_BOARD, row_index, 0
        elif(col == 'F' or col == 'f'):
            return WHITE_BOARD, row_index, 1
        elif(col == 'G' or col == 'g'):
            return WHITE_BOARD, row_index, 2
        elif(col == 'H' or col == 'h'):
            return WHITE_BOARD, row_index, 3   
        else:
            return None, None, None
        
    def colIndexToLetter(self,color_side,col_index):
        if(color_side == 0):
            if(col_index == 0):
                return 'A'
            elif(col_index == 1):
                return 'B'
            elif(col_index == 2):
                return 'C'
            elif(col_index == 3):
                return 'D'
            else:
                return None
        elif(color_side == 1):
            if(col_index == 0):
                return 'E'
            elif(col_index == 1):
                return 'F'
            elif(col_index == 2):
                return 'G'
            elif(col_index == 3):
                return 'H'
            else:
                return None
        else:
            return None
        
    
    # =============================================================================
    #  PASSIVE MOVE   
    # =============================================================================
    
    # receives input from user to select desired piece; returns piece coordinates
    
    def selectPiece(self, color) :     
        while(True):
            print("\nPassive Move:", end="")
            row_from, col_from = input("Select a "+color+" piece from your homeboard (<row> <column>): ").split()
            color_side, row_index, col_index = self.parseInput(row_from, col_from)
            
            if(color_side is None or row_index is None or col_index is None):
                print("INVALID INPUT")
                continue

            if((self.player == 0 and self.board.boards[WHITE_HB][color_side][row_index][col_index] == 'W') or
               (self.player == 1 and self.board.boards[BLACK_HB][color_side][row_index][col_index] == 'B')):          
                return color_side, row_index, col_index
            else:
                print("CHOOSE A PIECE OF YOUR COLOR")


    # displays board with an 'x' in the available passive move options; returns options
        
    def legalPassiveMoves(self, color_side, row_index, col_index):
        
        aux_board = Board()
        aux_board.boards = copy.deepcopy(self.board.boards)
        options = []
        
        for i in range(row_index - 2, row_index + 3): #2 rows behind, 2 rows ahead
             if(i < 0 or i > 3): 
                 continue
             for j in range(col_index - 2, col_index + 3): #2 cols behind, 2 cols ahead
                 if(j < 0 or j > 3): 
                     continue
                 
                 # efeito asterisco
                 if(((i == row_index - 2 or i == row_index + 2) and (j == col_index - 1 or j == col_index + 1)) or 
                    (((i == row_index - 1 or i == row_index + 1) and (j == col_index - 2 or j == col_index + 2)))):
                     continue
                 
                 if(self.board.boards[self.player][color_side][i][j] == ' '):
                     aux_board.boards[self.player][color_side][i][j] = 'x'
                     options.append([i,j])
        
        aux_board.display()
        
        return options
    
    # displays passive move options, lets user select desired one; returns desired move offset from piece cell (or 0 if player wants to re-select piece option)
    def passiveMoveOptions(self, options, color_side, row_index, col_index):
                
        print("\nPassive move options:")
        print("0: re-select piece")
        counter = 1
        for option in options:
            print(str(counter)+": "+ str(option[0]+1) + str(self.colIndexToLetter(color_side, option[1])))
            counter += 1
         
        while(True) :
            selected_option = input("Select an option (<option_number>):")
            parsed_selected_option = self.parseInt(selected_option)
            
            if(parsed_selected_option is None or parsed_selected_option < 0 or parsed_selected_option > len(options)):
                print("INVALID INPUT")
            
            # if option selected, return [row_offset, col_offset]
            elif(parsed_selected_option != 0): 
                target_row = options[parsed_selected_option-1][0]
                target_col = options[parsed_selected_option-1][1]
                return [target_row-row_index,target_col-col_index]
            
            # re-select piece option 
            else:
                return None
            
    # passive move function; returns passive move offset and the color side it was choosen from
        
    def passiveMove(self, color) :
        while(True):
            
            self.board.display()
                
            print("\n"+color+" player's turn:")
            
            color_side, row_index, col_index = self.selectPiece(color.lower())
            
            options = self.legalPassiveMoves(color_side, row_index, col_index)
            
            offset = self.passiveMoveOptions(options, color_side, row_index, col_index)
            
            if(offset is not None):
                break
            
        return offset, color_side
        
    
    # =============================================================================
    #  AGRESSIVE MOVE   
    # =============================================================================
    
    # receives cell coordinates and passive move offset, checks if it's possible; returns True/False
    
    def verifyDirection(self, player_side, color_side, row, col, offset, piece, other_piece):
        
        if(row + offset[0] not in [0,1,2,3] or col + offset[1] not in [0,1,2,3]):
            #print(row + offset[0], col + offset[1])
            return False # out of board move
        
        v_dir = 0
        h_dir = 0
        
        if(offset[0] != 0):
            v_dir = int(offset[0] / abs(offset[0]))
        if(offset[1] != 0):
            h_dir = int(offset[1] / abs(offset[1]))
            
        n_iter = max(abs(offset[0]),abs(offset[1]))
        
        pushing = False
        
        for i in range(1, n_iter + 1):
            if(self.board.boards[player_side][color_side][row + i*v_dir][col + i*h_dir] == piece):
                return False # cannot push own piece
            if(self.board.boards[player_side][color_side][row + i*v_dir][col + i*h_dir] == other_piece):
                pushing = True # found other color piece to push
            if(pushing): # pushing a piece. Check that the next cell doesnt have a piece (is empty or out of board)
                if(row + (i+1)*v_dir in [0,1,2,3] and col + (i+1)*h_dir in [0,1,2,3]): # if inside board
                    if(self.board.boards[player_side][color_side][row + (i+1)*v_dir][col + (i+1)*h_dir] != " "): # if not empty
                        return False
                    
        return True

    # receives passive move offset and returns all possible options for the agressive move

    def legalAgressiveMoves(self, offset, color_side, color):
                
        if(color == "Black"):
            piece = "B"
            other_piece = "W"
        else:
            piece = "W"
            other_piece = "B"
        

        other_color = self.switch_01(color_side)
    
        options1 = []
        options2 = []
    
        for row in range(4):
            for col in range(4):
                if(self.board.boards[0][other_color][row][col] == piece):
                    if(self.verifyDirection(0, other_color, row, col, offset, piece, other_piece)):
                        options1.append([row,col])
                if(self.board.boards[1][other_color][row][col] == piece):
                    if(self.verifyDirection(1, other_color, row, col, offset, piece, other_piece)):
                        options2.append([row,col])
        
        return [options1, options2]

    # displays agressive move options and lets player choose one; returns selected piece (or 0 if player wants to re-select passive move)

    def agressiveMoveOptions(self, color_side, options):
        print("\nAgressive move options:")
        print("0: re-select passive move")
        counter = 1
        for option in options[0]:
            print(str(counter)+": "+ str(option[0]+1) + str(self.colIndexToLetter(color_side, option[1])))
            counter += 1
            
        split = counter 
        
        for option in options[1]:
           print(str(counter)+": "+ str(option[0]+5) + str(self.colIndexToLetter(color_side, option[1])))
           counter += 1
        
        while(True) :
            selected_option = input("Select an option (<option_number>):")
            parsed_selected_option = self.parseInt(selected_option)
            
            if(parsed_selected_option is None or parsed_selected_option < 0 or parsed_selected_option > len(options)):
                print("INVALID INPUT")
            
            # if option selected, return selected cell coords
            elif(parsed_selected_option != 0):
                if(parsed_selected_option < split): # if selected option < split, move is in white's homeboards
                    return options[0][parsed_selected_option-1], 0
                else: # else, move is in black's homeboards
                    return options[1][parsed_selected_option-1], 1
            
            # re-select passive move 
            else:
                return None, None


    def agressiveMove(self, offset, color_side, color):     
        options = self.legalAgressiveMoves(offset, color_side, color)
        selected, player_side = self.agressiveMoveOptions(color_side, options)
        if(selected is None):
            return None # re-select passive Move
        else:
            return True
        
        



    def turn(self):
        
        if(self.player):
            color = 'Black'
        else: 
            color = 'White'
            
        while(True):
            offset, color_side = self.passiveMove(color)
            result = self.agressiveMove(offset, color_side, color)
            if(result is not None):
                break
       
    

def main() :
    game = GameLogic()
    game.turn()
    
main()
