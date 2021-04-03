import numpy
import signal
import sys
import time
import timeit
import random

def signal_handler(sig, frame):
    print('\n\nExiting...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# =============================================================================
#  CONSTANTS
# =============================================================================

# white player homeboard (cima); has one black board and one white board
WHITE_HB = 0
# black player homeboard (baixo); has one black board and one white board
BLACK_HB = 1
BLACK_BOARD = 0  # black colored boards (left side boards)
WHITE_BOARD = 1  # white colored boards (right side boards)


class Board:
    def __init__(self):

        #Parameters for evaluation function
        self.points_per_piece = 100
        self.points_per_extra_piece = [100,200,300]
        self.points_per_extra_piece_turn = [40,30,20,10]
        self.points_per_unique_vulnerable = 20  # total unique pieces vulnerable on a given board
        self.points_per_insecure = 1     # total attacks that kill on all pieces of a given board
        self.points_per_unique_secure = 15    # total unique secure pieces on a given board


        self.boards = [[[['W', 'W', 'W', 'W'],
                         [' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' '],
                         ['B', 'B', 'B', 'B']],

                        [['W', 'W', 'W', 'W'],
                         [' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' '],
                         ['B', 'B', 'B', 'B']]],

                       [[['W', 'W', 'W', 'W'],
                         [' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' '],
                         ['B', 'B', 'B', 'B']],

                        [['W', 'W', 'W', 'W'],
                         [' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' '],
                         ['B', 'B', 'B', 'B']]]]
        
                               
                        
    def displayHomeboard(self, color, color_string, row_number):

        print("   _______________________  |  _______________________ ")

        for row in range(4):
            print("  |     |     |     |     | | |     |     |     |     |")
            print(row_number, end=" ")  # row label

            for black_cell in range(4):  # print row from black board
                print("|  " + self.boards[color][BLACK_BOARD]
                      [row][black_cell] + "  ", end="")
            print("| | ", end="")
            for white_cell in range(4):  # print row from white board
                print("|  " + self.boards[color][WHITE_BOARD]
                      [row][white_cell] + "  ", end="")

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
    
        
    def countNumPieces(self):
        score_num_pieces = []
        for homeboard in range(2):
            for board in range(2):
                num_black = numpy.count_nonzero(self.boards[homeboard][board] == "B")
                num_white = numpy.count_nonzero(self.boards[homeboard][board] == "W")
                score_num_pieces.append([num_white, num_black])
        return score_num_pieces
    
    def calcDiffNumPieces(self, boards_num_pieces, player):
        
        individual_board_scores = []
        for board_num_pieces in boards_num_pieces:
            if(board_num_pieces[0] == 0): # 0 white pieces, black won
                score = -100000000
            elif(board_num_pieces[1] == 0): # 0 black pieces, white won
                score = 100000000
            else:
                # +/- points_per_piece
                score = (board_num_pieces[0] - board_num_pieces[1])*self.points_per_piece 
                
                # value white base on how many black pieces left
                if(board_num_pieces[1] == 1): # 1 black piece left
                    score += self.points_per_extra_piece[0]
                elif(board_num_pieces[1] == 2): # 2 black piece left
                    score += self.points_per_extra_piece[1]          
                elif(board_num_pieces[1] == 3): # 3 black piece left
                    score += self.points_per_extra_piece[2]
                
                # value black base on how many white pieces left
                if(board_num_pieces[0] == 1): # 1 white piece left
                    score -= self.points_per_extra_piece[0]
                elif(board_num_pieces[0] == 2): # 2 white piece left
                    score -= self.points_per_extra_piece[1]
                elif(board_num_pieces[0] == 3): # 3 white piece left
                    score -= self.points_per_extra_piece[2]
                
                # value player's turn
                if(player): # black to move
                    if(board_num_pieces[0] == 1): # 1 pieces left
                        score -= self.points_per_extra_piece_turn[0]
                    elif(board_num_pieces[0] == 2): # 2 piece left
                        score -= self.points_per_extra_piece_turn[1]
                    elif(board_num_pieces[0] == 3): # 3 pieces left
                        score -= self.points_per_extra_piece_turn[2] 
                    else: # 4 piece left
                        score -= self.points_per_extra_piece_turn[3]
                else: # white to move
                    if(board_num_pieces[0] == 1): # 1 pieces left
                        score += self.points_per_extra_piece_turn[0]
                    elif(board_num_pieces[0] == 2): # 2 piece left
                        score += self.points_per_extra_piece_turn[1]
                    elif(board_num_pieces[0] == 3): # 3 pieces left
                        score += self.points_per_extra_piece_turn[2]
                    else: # 4 piece left
                        score += self.points_per_extra_piece_turn[3]
                    
                            
            individual_board_scores.append(score)
        
        return individual_board_scores

      
# easy -> calcDiff
# medium -> meter ao quadrado
# hard -> tudo


# -avaliaçao em ampulheta:
#     -um board inimigo é tao bom quanto melhor for o board na diagonal (ataque)
#     -um board amigo é tao bom quanto melhor for o board na horizontal (ataque e fuga)

    def calcPoints(self, player, difficulty, gameLogic):
              
        boards_num_pieces = self.countNumPieces()

        individual_board_scores = self.calcDiffNumPieces(boards_num_pieces, player)

        final_score = individual_board_scores[0]*abs(individual_board_scores[0]) + individual_board_scores[1]*abs(individual_board_scores[1]) + individual_board_scores[2]*abs(individual_board_scores[2]) + individual_board_scores[3]*abs(individual_board_scores[3]) 
  

        return final_score
        

                
    def isNotRepeated(self, repeated):
        for board in repeated:
            if(numpy.array_equal(self.boards, board.boards, equal_nan=False)):
                return False
        return True
        
    

class GameLogic:
    def __init__(self):
        self.board = Board()
        self.player = 1  # white=0, black=1
        
        self.score = {0:0, 1:0} #scores initialized with 0, need this to minmax 
        self.boards_history = [] #boards that have already been played, in order to avoid them
        
        self.playerColor = None
        self.difficulty = None # 1.Easy 2.Medium 3.Hard
        self.difficultyWhite = None
        self.difficultyBlack = None
        self.cntComWhiteMove = 0 #number or computer white moves
        self.cntComBlackMove = 0

    # =============================================================================
    #  AUX FUNTIONS
    # =============================================================================

    # 1 - 1 = 0; 1 - 0 = 1

    def switch_01(self, number):
        return 1 - number

    def parseInt(self, x):
        try:
            int_x = int(x)
            return int_x
        except ValueError:
            return None

    def parseInput(self, cell_input):

        if(len(cell_input) != 2):
            return None, None, None, None

        row = cell_input[0]
        col = cell_input[1]

        int_row = self.parseInt(row)
        if(int_row is None or int_row < 1 or int_row > 8):
            return None, None, None, None

        if(int_row <= 4):
            player_side = WHITE_HB
        else:
            player_side = BLACK_HB

        row_index = (int_row - 1) % 4

        if(col == 'A' or col == 'a'):
            return player_side, BLACK_BOARD, row_index, 0
        elif(col == 'B' or col == 'b'):
            return player_side, BLACK_BOARD, row_index, 1
        elif(col == 'C' or col == 'c'):
            return player_side, BLACK_BOARD, row_index, 2
        elif(col == 'D' or col == 'd'):
            return player_side, BLACK_BOARD, row_index, 3

        elif(col == 'E' or col == 'e'):
            return player_side, WHITE_BOARD, row_index, 0
        elif(col == 'F' or col == 'f'):
            return player_side, WHITE_BOARD, row_index, 1
        elif(col == 'G' or col == 'g'):
            return player_side, WHITE_BOARD, row_index, 2
        elif(col == 'H' or col == 'h'):
            return player_side, WHITE_BOARD, row_index, 3
        else:
            return None, None, None, None

    def colIndexToLetter(self, color_side, col_index):
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

    def displayArrow(self, arrow, n_arrows):
        for i in range(n_arrows):
            print(arrow, end="")
        print("")

    def displayOffset(self, row_offset, col_offset):

        n_arrows = max(abs(row_offset), abs(col_offset))

        if(row_offset < 0):  # up
            if(col_offset < 0):  # left
                self.displayArrow("↖", n_arrows)
            elif(col_offset > 0):  # right
                self.displayArrow("↗", n_arrows)
            else:  # up
                self.displayArrow("↑", n_arrows)
        elif(row_offset > 0):  # down
            if(col_offset < 0):  # left
                self.displayArrow("↙", n_arrows)
            elif(col_offset > 0):  # right
                self.displayArrow("↘", n_arrows)
            else:  # up
                self.displayArrow("↓", n_arrows)
        else:  # sides
            if(col_offset < 0):  # left
                self.displayArrow("←", n_arrows)
            else:  # right
                self.displayArrow("→", n_arrows)

    # =============================================================================
    #  PASSIVE MOVE
    # =============================================================================

    # receives input from user to select desired piece; returns piece coordinates

    def selectPiece(self, color):
        while(True):

            cell_input = input("Select a "+color +
                               " piece from your homeboard (<row><column>): ")

            player_side, color_side, row_index, col_index = self.parseInput(
                cell_input)

            if(color_side is None or row_index is None or col_index is None):
                print("INVALID INPUT")
                continue

            if(player_side != self.player):
                print("CHOOSE A PIECE FROM ONE OF YOUR HOMEBOARDS")
            else:
                if((self.player == 0 and self.board.boards[WHITE_HB][color_side][row_index][col_index] == 'W') or
                   (self.player == 1 and self.board.boards[BLACK_HB][color_side][row_index][col_index] == 'B')):
                    return color_side, row_index, col_index
                else:
                    print("CHOOSE A PIECE OF YOUR COLOR")

    # displays board with an 'x' in the available passive move options; returns options

    def legalPassiveMoves(self, board, homeboard, color_side, row_index, col_index, is_human):

        if(is_human):
            aux_board = Board()
            # aux_board.boards = copy.deepcopy(board.boards)            
            # aux_board.boards = board.copyBoard()
            aux_board.boards = numpy.copy(board.boards)
        options = []

        for i in range(row_index - 2, row_index + 3):  # 2 rows behind, 2 rows ahead
            if(i < 0 or i > 3):
                continue
            for j in range(col_index - 2, col_index + 3):  # 2 cols behind, 2 cols ahead
                if(j < 0 or j > 3):
                    continue

                # skips any cell that doesnt satisfy an * format
                if(((i == row_index - 2 or i == row_index + 2) and (j == col_index - 1 or j == col_index + 1)) or
                   (((i == row_index - 1 or i == row_index + 1) and (j == col_index - 2 or j == col_index + 2)))):
                    continue

                # skips options that need to jump over pieces
                if(i == row_index - 2 or i == row_index + 2 or
                   j == col_index - 2 or j == col_index + 2):
                    middle_i = int((row_index + i)/2)
                    middle_j = int((col_index + j)/2)
                    if(board.boards[homeboard][color_side][middle_i][middle_j] != ' '):
                        continue
                
                if(board.boards[homeboard][color_side][i][j] == ' '):
                    options.append([i, j])
                    if(is_human):
                        aux_board.boards[homeboard][color_side][i][j] = 'x'
                    

        if(is_human):
            aux_board.display()

        return options

    # displays passive move options, lets user select desired one; returns desired move offset from piece cell (or 0 if player wants to re-select piece option)
    def passiveMoveOptions(self, options, color_side, row_index, col_index):

        print("\nPassive move options:")
        print("0: re-select piece")
        counter = 1

        if(self.player):  # black player => black homeboard => row in [5,6,7,8]
            board_offset = 5
        else:  # white player => white homeboard => row in [1,2,3,4]
            board_offset = 1

        for option in options:
            print(str(counter)+": " + str(option[0]+board_offset) +
                  str(self.colIndexToLetter(color_side, option[1])))
            counter += 1

        while(True):
            selected_option = input("Select an option (<option_number>):")
            parsed_selected_option = self.parseInt(selected_option)

            if(parsed_selected_option is None or parsed_selected_option < 0 or parsed_selected_option > len(options)):
                print("INVALID INPUT")

            # if option selected, return [row_offset, col_offset]
            elif(parsed_selected_option != 0):
                target_row = options[parsed_selected_option-1][0]
                target_col = options[parsed_selected_option-1][1]
                return [target_row-row_index, target_col-col_index]

            # re-select piece option
            else:
                return None

    # passive move function; returns passive selected piece, the move offset and the color side it was choosen from

    def passiveMove(self, color):
        while(True):

            print("\n> > "+color+" player's turn:")

            print("\n> Passive Move:")

            color_side, row_index, col_index = self.selectPiece(color.lower())

            options = self.legalPassiveMoves(self.board, self.player, color_side, row_index, col_index, True)

            offset = self.passiveMoveOptions(
                options, color_side, row_index, col_index)

            if(offset is not None):
                break

        return offset, color_side, [row_index, col_index]

    # =============================================================================
    #  AGRESSIVE MOVE
    # =============================================================================

    # receives cell coordinates and passive move offset, checks if it's possible; returns True/False

    def verifyDirection(self, board, player_side, color_side, row, col, offset, piece, other_piece):

        if(row + offset[0] not in [0, 1, 2, 3] or col + offset[1] not in [0, 1, 2, 3]):
            # print(row + offset[0], col + offset[1])
            return False  # out of board move

        v_dir = 0
        h_dir = 0

        if(offset[0] != 0):
            v_dir = int(offset[0] / abs(offset[0]))
        if(offset[1] != 0):
            h_dir = int(offset[1] / abs(offset[1]))

        n_iter = max(abs(offset[0]), abs(offset[1]))

        pushing = False

        for i in range(1, n_iter + 1):
            if(board.boards[player_side][color_side][row + i*v_dir][col + i*h_dir] == piece):
                return False  # cannot push own piece
            if(board.boards[player_side][color_side][row + i*v_dir][col + i*h_dir] == other_piece):
                pushing = True  # found other color piece to push
            if(pushing):  # pushing a piece. Check that the next cell doesnt have a piece (is empty or out of board)
                # if inside board
                if(row + (i+1)*v_dir in [0, 1, 2, 3] and col + (i+1)*h_dir in [0, 1, 2, 3]):
                    # if not empty
                    if(board.boards[player_side][color_side][row + (i+1)*v_dir][col + (i+1)*h_dir] != " "):
                        return False

        return True

    # receives passive move offset and returns all possible options for the agressive move

    def legalAgressiveMoves(self, board, offset, other_color, piece, other_piece):

        options1 = []
        options2 = []

        for row in range(4):
            for col in range(4):
                if(board.boards[0][other_color][row][col] == piece):
                    if(self.verifyDirection(board, 0, other_color, row, col, offset, piece, other_piece)):
                        options1.append([row, col])
                if(board.boards[1][other_color][row][col] == piece):
                    if(self.verifyDirection(board, 1, other_color, row, col, offset, piece, other_piece)):
                        options2.append([row, col])

        return [options1, options2]

    # gets all legal moves and returns four lists with passive and agressive from each player

    def getLegalMoves(self, gameboard, repeated, player):

        #start_time = timeit.default_timer()

        moves = []
        
        for homeboard in range(2):
            for board in range(2):
                for row in range(4):
                    for col in range(4):
                        if(player == 1 and gameboard.boards[homeboard][board][row][col] == "B" and homeboard == 1): # If black player and black piece on black HB
                            passive_moves = self.legalPassiveMoves(gameboard ,homeboard, board, row, col, False)
                            for passive_move in passive_moves:
                                offset = [passive_move[0]-row, passive_move[1]-col]
                                other_color = self.switch_01(board)
                                agressive_moves = self.legalAgressiveMoves(gameboard, offset, other_color, "B", "W")
                                
                                for agressive_move in agressive_moves[0]:
                                    aux_board = Board()
                                    # aux_board.boards = copy.deepcopy(gameboard.boards)
                                    # aux_board.boards = gameboard.copyBoard()
                                    aux_board.boards = numpy.copy(gameboard.boards)
                                    self.updateBoard([homeboard,board,row,col], [0,other_color,agressive_move[0],agressive_move[1]], offset, "B", "W", aux_board)
                                    if(aux_board.isNotRepeated(repeated)):
                                        moves.append([[homeboard,board,row,col], [0,other_color,agressive_move[0],agressive_move[1]], offset])
                                
                                for agressive_move in agressive_moves[1]:
                                    aux_board = Board()
                                    # aux_board.boards = copy.deepcopy(gameboard.boards)
                                    # aux_board.boards = gameboard.copyBoard()
                                    aux_board.boards = numpy.copy(gameboard.boards)
                                    self.updateBoard([homeboard,board,row,col], [1,other_color,agressive_move[0],agressive_move[1]], offset, "B", "W", aux_board)
                                    if(aux_board.isNotRepeated(repeated)):
                                        moves.append([[homeboard,board,row,col], [1,other_color,agressive_move[0],agressive_move[1]], offset])

                        elif(player == 0 and gameboard.boards[homeboard][board][row][col] == "W" and homeboard == 0): #If white player and white piece on white HB
                            passive_moves = self.legalPassiveMoves(gameboard ,homeboard, board, row, col, False)
                            for passive_move in passive_moves:
                                offset = [passive_move[0]-row, passive_move[1]-col]
                                other_color = self.switch_01(board)
                                agressive_moves = self.legalAgressiveMoves(gameboard, offset, other_color, "W", "B")
                                
                                for agressive_move in agressive_moves[0]:
                                    aux_board = Board()
                                    # aux_board.boards = copy.deepcopy(gameboard.boards)
                                    # aux_board.boards = gameboard.copyBoard()
                                    aux_board.boards = numpy.copy(gameboard.boards)
                                    self.updateBoard([homeboard,board,row,col], [0,other_color,agressive_move[0],agressive_move[1]], offset, "W", "B", aux_board)
                                    if(aux_board.isNotRepeated(repeated)):
                                        moves.append([[homeboard,board,row,col], [0,other_color,agressive_move[0],agressive_move[1]], offset])
                                    
                                for agressive_move in agressive_moves[1]:
                                    aux_board = Board()
                                    # aux_board.boards = copy.deepcopy(gameboard.boards)
                                    # aux_board.boards = gameboard.copyBoard()
                                    aux_board.boards = numpy.copy(gameboard.boards)
                                    self.updateBoard([homeboard,board,row,col], [1,other_color,agressive_move[0],agressive_move[1]], offset, "W", "B", aux_board)
                                    if(aux_board.isNotRepeated(repeated)):
                                        moves.append([[homeboard,board,row,col], [1,other_color,agressive_move[0],agressive_move[1]], offset])

        #elapsed = timeit.default_timer() - start_time
        #print("Elapsed Time on Legal Moves: ", elapsed)

        return moves



    # displays agressive move options and lets player choose one; returns selected piece (or 0 if player wants to re-select passive move)

    def agressiveMoveOptions(self, color_side, options):

        print("\nAgressive move options:")

        if(options == [[], []]):
            print("\nNo valid agressive moves. Please select a new passive move.")
            time.sleep(3)
            return None, None

        print("0: re-select passive move")
        counter = 1
        for option in options[0]:
            print(str(counter)+": " +
                  str(option[0]+1) + str(self.colIndexToLetter(color_side, option[1])))
            counter += 1

        split = counter

        for option in options[1]:
            print(str(counter)+": " +
                  str(option[0]+5) + str(self.colIndexToLetter(color_side, option[1])))
            counter += 1

        while(True):
            selected_option = input("Select an option (<option_number>):")
            parsed_selected_option = self.parseInt(selected_option)

            if(parsed_selected_option is None or parsed_selected_option < 0 or parsed_selected_option > (len(options[0]) + len(options[1]))):
                print("INVALID INPUT")

            # if option selected, return selected cell coords
            elif(parsed_selected_option != 0):
                # if selected option < split, move is in white's homeboards
                if(parsed_selected_option < split):
                    return options[0][parsed_selected_option-1], 0
                else:  # else, move is in black's homeboards
                    return options[1][parsed_selected_option-split], 1

            # re-select passive move
            else:
                return None, None

    # agressive move function; returns agressive selected piece and the color side it was choosen from

    def agressiveMove(self, offset, other_color, piece, other_piece):

        print("\n> Agressive Move:")

        print("\nSelected movement: ", end="")
        self.displayOffset(offset[0], offset[1])

        options = self.legalAgressiveMoves(
           self.board, offset, other_color, piece, other_piece)
        selected, player_side = self.agressiveMoveOptions(other_color, options)

        if(selected is None):
            return None, None  # re-select passive Move
        else:
            return selected, player_side

    # receives selected passive and agressive pieces, the move offset and the player and enemy player's pieces; returns True if an enemy piece was pushed out of the board, else False

    def updateBoard(self, passive_piece, agressive_piece, offset, piece, other_piece, board):
        
        
        if(board.boards[passive_piece[0]][passive_piece[1]][passive_piece[2]][passive_piece[3]] == ' '
           or board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2]][agressive_piece[3]] == ' '):
            print("Panic")
            print(passive_piece)
            print(agressive_piece)
            print(offset)
            print(piece)
            exit()
            
            
        
        board.boards[passive_piece[0]][passive_piece[1]][passive_piece[2]][passive_piece[3]] = ' '
        board.boards[passive_piece[0]][passive_piece[1]][passive_piece[2] + offset[0]][passive_piece[3] + offset[1]] = piece

        board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2]][agressive_piece[3]] = ' '

        v_dir = 0
        h_dir = 0

        if(offset[0] != 0):
            v_dir = int(offset[0] / abs(offset[0]))
        if(offset[1] != 0):
            h_dir = int(offset[1] / abs(offset[1]))

        n_iter = max(abs(offset[0]), abs(offset[1]))

        pushing = False
        coord_piece_pushed = None
        for i in range(1, n_iter + 1):
            if(board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2] + i*v_dir][agressive_piece[3] + i*h_dir] == other_piece):
                pushing = True  # is pushing other color piece
                coord_piece_pushed = [agressive_piece[0],agressive_piece[1],agressive_piece[2] + i*v_dir,agressive_piece[3] + i*h_dir] 
            if(i == n_iter):  # if in last cell of the offset, place the piece
                board.boards[agressive_piece[0]][agressive_piece[1]
                                                      ][agressive_piece[2] + i*v_dir][agressive_piece[3] + i*h_dir] = piece
            else:  # else, clean the path
                board.boards[agressive_piece[0]][agressive_piece[1]
                                                      ][agressive_piece[2] + i*v_dir][agressive_piece[3] + i*h_dir] = ' '

        if(pushing):  # if there's enemy piece to be pushed
            # if destiny location is in board, update it
            if(agressive_piece[2] + offset[0] + v_dir in [0, 1, 2, 3] and agressive_piece[3] + offset[1] + h_dir in [0, 1, 2, 3]):
                board.boards[agressive_piece[0]][agressive_piece[1]][agressive_piece[2] +
                                                                          offset[0] + v_dir][agressive_piece[3] + offset[1] + h_dir] = other_piece
            else:
                return [True, pushing, coord_piece_pushed]  # enemy piece was pushed out of board => check for winners

        return [False, pushing, coord_piece_pushed]  # no enemy piece was pushed out of the board => no need to check for winners

    # makes a passive and aggresive move based on the game mode and the color of the player to move; returns True if an enemy piece was pushed out of the board, else False



    def playerMove(self, color, piece, other_piece):
        while(True):
            offset, color_side, passive_selected = self.passiveMove(color)
    
            other_color = self.switch_01(color_side)
    
            agressive_selected, player_side = self.agressiveMove(
                offset, other_color, piece, other_piece)
    
            if(agressive_selected is not None and player_side is not None):
                break
            
        return self.updateBoard([self.player, color_side, passive_selected[0], passive_selected[1]],
                                [player_side, other_color, agressive_selected[0], agressive_selected[1]],
                                offset, piece, other_piece, self.board)[0]

    def computerMove(self, color, depth, prune, piece, other_piece):
        
        maximizing = False
        if(color == 'White'):
            maximizing = True
            self.cntComWhiteMove += 1
            if self.difficultyWhite == 0 or self.difficulty == 0: #Super Easy
                legal_moves = self.getLegalMoves(self.board,[],0)
                length = len(legal_moves) - 1
                if length < 0:
                    print ("Black Won, white has no moves")
                    os.exit(0)
                index = random.randrange(0,length)
                best_move = legal_moves[index]
                return self.updateBoard(best_move[0], best_move[1], best_move[2], piece, other_piece, self.board)[0]
            elif self.difficultyWhite == 1 or self.difficulty == 1: #Easy
                depth = 1
            elif self.difficultyWhite == 2 or self.difficulty == 2: #Medium
                depth = 2
            elif self.difficultyWhite == 3 or self.difficulty == 3: #Hard
                depth = 3
            elif self.difficultyWhite == 4 or self.difficulty == 4: #Dynamic Hard
                depth = 2
                if self.cntComWhiteMove > 5:
                    depth = 3
        else:
            self.cntComBlackMove += 1
            if self.difficultyBlack == 0 or self.difficulty == 0: #Super Easy
                legal_moves = self.getLegalMoves(self.board,[],1)
                length = len(legal_moves) - 1
                if length < 0:
                    print ("White Won, black has no moves")
                    os.exit(0)
                index = random.randrange(0,length)
                best_move = legal_moves[index]
                return self.updateBoard(best_move[0], best_move[1], best_move[2], piece, other_piece, self.board)[0]
            elif self.difficultyBlack == 1 or self.difficulty == 1: #Easy
                depth = 1
            elif self.difficultyBlack == 2 or self.difficulty == 2: #Medium
                depth = 2
            elif self.difficultyBlack == 3 or self.difficulty == 3: #Hard
                depth = 3
            elif self.difficultyBlack == 4 or self.difficulty == 4: #Dynamic Hard
                depth = 2
                if self.cntComBlackMove > 5:
                    depth = 3
 
        best_move = self.minimax(self.board, self.boards_history, depth, depth, -sys.maxsize, sys.maxsize, maximizing, self.player, piece, other_piece)
        return self.updateBoard(best_move[1], best_move[2], best_move[3], piece, other_piece, self.board)[0]



    def makeMove(self, color, piece, other_piece, depth, prune):
        if(self.mode == 1): #PvP         
            return self.playerMove(color, piece, other_piece)
                
        elif(self.mode == 2): # PvC
        
            # Player move               
            if(self.player == self.playerColor):
                return self.playerMove(color, piece, other_piece)  
            else:
                return self.computerMove(color, depth, prune, piece, other_piece)
                

        else: # CvC
            return self.computerMove(color, depth, prune, piece, other_piece)


    # calls passive and agressive move functions; returns True if an enemy piece was pushed out of the board, else False

    def turn(self):

        if(self.player):
            color = 'Black'
            piece = "B"
            other_piece = "W"
        else:
            color = 'White'
            piece = "W"
            other_piece = "B"

        enemyPushedOff = self.makeMove(color, piece, other_piece, 5, True)

        aux_board = Board()
        # aux_board.boards = copy.deepcopy(self.board)
        # aux_board.boards = self.board.copyBoard()
        aux_board.boards = numpy.copy(self.board.boards)
        
        self.boards_history.append(aux_board)

        return  enemyPushedOff



    # checks for a winner in a board; if winner, returns the winning color, else false

    def isThereWinnerInBoard(self, i, j):

        whites = 0
        blacks = 0
        for row in range(4):
            for col in range(4):
                if(self.board.boards[i][j][row][col] == 'W'):  # found a white piece
                    whites += 1
                elif(self.board.boards[i][j][row][col] == 'B'):  # found a black piece
                    blacks += 1
                if(whites != 0 and blacks != 0):  # board with both pieces, no winner on this board
                    return False

        # if function reaches here, there is a winner
        if(whites != 0):
            return "WHITE"
        else:
            return "BLACK"

    # checks for a winner in all boards

    def isThereWinner(self):
        for i in range(2):
            for j in range(2):
                winner = self.isThereWinnerInBoard(i, j)
                if(winner):
                    return winner
        return False

    # choose gamemode and difficulty

    def menu(self):
        print("\n=====================================================================")
        print("\n====                           SHOBU                             ====")
        print("\n=====================================================================")
        print("\n\n====                           MENU                              ====")
        print("\n\n    1. Player VS Player                         2.Player VS COM        ")
        print("\n                           3. COM VS COM                             ")

        mode = 0
        while(mode < 1 or mode > 3):
            mode = int(input("\nChoose a game mode: "))
        self.mode = mode

        if(mode == 2):
            playerColor = 0
            print("\n   1.White                                          2.Black   ")
            while(playerColor < 1 or playerColor > 3):
                playerColor = int(input("\nChoose your Color: "))
            self.playerColor = playerColor - 1
            

            difficulty = 0
            print("\n 0.Super Easy     1.Easy         2.Medium          3.Hard         4.Dynamic Hard")
            while(difficulty < 1 or difficulty > 4):
                difficulty = int(input("\nChoose difficulty for COM: "))
            self.difficulty = difficulty

        if(mode == 3):
            difficultyWhite = -1
            print("\n 0.Super Easy     1.Easy         2.Medium          3.Hard         4.Dynamic Hard")
            while(difficultyWhite < 0 or difficultyWhite > 4):
                difficultyWhite = int(input("\nChoose difficulty for White: "))
            self.difficultyWhite = difficultyWhite

            difficultyBlack = -1
            print("\n 0.Super Easy     1.Easy         2.Medium          3.Hard         4.Dynamic Hard")
            while(difficultyBlack < 0 or difficultyBlack > 4):
                difficultyBlack = int(input("\nChoose difficulty for Black: "))
            self.difficultyBlack = difficultyBlack

    def run(self):
        sum=0
        while(True):
            start_time = timeit.default_timer()
            self.board.display()
            if(self.turn()):
                winner = self.isThereWinner()
                if(winner):
                    break
            self.player = self.switch_01(self.player)
            if(self.player == 0):
                print("WHITE TURN")
            else:
                print("BLACK TURN")
            print(
                "\n=====================================================================")
            elapsed = timeit.default_timer() - start_time
            print("||||||||| Elapsed Time on This Turn: ", elapsed)
            sum+= elapsed
        print("\n=====================================================================")
        self.board.display()
        print("\nGAME OVER! WINNER IS: " + winner)
        print("Total Time: ", sum)

    
    def sortMoves(self, board, repeated, turn, piece, other_piece, difficulty):

        
        start_time1 = timeit.default_timer()
        moves = self.getLegalMoves(board, repeated, turn)
        elapsed1 = timeit.default_timer() - start_time1
        #print("- getLegal: ", elapsed1)
        
        
        move_scores = []
        elapsed2 = 0
        
        if(difficulty == 3):
            difficulty == 2
        
        for move in moves:
            updated_board = Board()
            # updated_board.boards = copy.deepcopy(board.boards)
            # updated_board.boards = board.copyBoard()
            updated_board.boards = numpy.copy(board.boards)
            self.updateBoard(move[0], move[1], move[2], piece, other_piece, updated_board)
            
            start_time2 = timeit.default_timer()
            move_score = board.calcPoints(turn, difficulty, self)
            elapsed2 += timeit.default_timer() - start_time2
            
            move_scores.append([move, move_score])
        #print("- calcPoints: ", elapsed2)



        if turn == 1:
            best_move = sorted(move_scores, key= lambda move_score : move_score[1]) #ascending order, for black
        else:
            best_move = sorted(move_scores, key= lambda move_score : move_score[1], reverse=True)

        #moves.remove(best_move[0])
        #moves.insert(0, best_move[0])
        return moves

    def minimax(self, board, repeated, depth_size, depth, alpha, beta, maximizing, turn, piece, other_piece):
        
        if(self.mode == 2):
            difficulty = self.difficulty
        elif(self.mode == 3):
            if(turn == 1): # black player
                difficulty = self.difficultyBlack
            else:
                difficulty = self.difficultyWhite
        else:
            exit()
        
        if depth == 0:
            return  [board.calcPoints(turn, difficulty, self), None, None, None]
        
        moves_sorted = self.getLegalMoves(board, repeated, turn)        
        turn = self.switch_01(turn) # change player pov
    
        if maximizing:      # white to play (wants to maximize score)
            best = [-sys.maxsize, None, None, None] 
            for move in moves_sorted:
                updated_board = Board()
                # updated_board.boards = board.copyBoard()
                updated_board.boards = numpy.copy(board.boards)
                self.updateBoard(move[0], move[1], move[2], piece, other_piece, updated_board)
                repeated.append(updated_board)     
                score = self.minimax(updated_board, repeated, depth_size, depth-1,alpha,beta,False,turn, other_piece, piece)
                repeated.pop()
                if(score[0] > best[0] or (score[0] == best[0] and random.randrange(0,4) == 3)): # score value > best value
                    if(depth == depth_size):
                        best = [score[0], move[0], move[1], move[2]]
                    else:
                        best[0] = score[0]
                alpha = max(alpha,best[0])
                if(alpha >= beta):
                    break    

        else: # black to play (wants to minimize score)
            best = [sys.maxsize, None, None, None] 
            for move in moves_sorted:
                updated_board = Board()
                # updated_board.boards = board.copyBoard()
                updated_board.boards = numpy.copy(board.boards)
                self.updateBoard(move[0], move[1], move[2], piece, other_piece, updated_board)
                repeated.append(updated_board)
                score = self.minimax(updated_board, repeated, depth_size, depth-1,alpha,beta,True,turn, other_piece, piece)
                repeated.pop()
                if(score[0] < best[0] or (score[0] == best[0] and random.randrange(0,4) == 3)): # score value < best value
                    if(depth == depth_size):
                        best = [score[0], move[0], move[1], move[2]]
                    else:
                        best[0] = score[0]
                beta = min(beta,best[0])
                if(beta <= alpha):
                    break
                
                    
        return best


def main():
    game = GameLogic()
    game.menu()
    game.run()


main()
