class HomeBoard:
    def __init__(self):
        self.color_boards = [[['W','W','W','W'],[' ',' ',' ',' '],[' ',' ',' ',' '],['B','B','B','B']], [['W','W','W','W'],[' ',' ',' ',' '],[' ',' ',' ',' '],['B','B','B','B']]]
        # white=0, black=1
        
    def display(self, color):
        print("   _______________________     _______________________ ")
        for row in range(4):
            print("  |     |     |     |     |   |     |     |     |     |")
            print(row+1, end=" ")
            for black_cell in range(4):
                print("|  " + self.color_boards[0][row][black_cell] + "  ", end="")
            print("|   ", end="")
            for white_cell in range(4):
                print("|  " + self.color_boards[1][row][black_cell] + "  ", end="")
            print("|\n  |_____|_____|_____|_____|   |_____|_____|_____|_____|", end="")
            if(row == 1):
                if(color == "white"):
                    print("   White's Homeboards", end="")
                else:
                    print("   Blacks's Homeboards", end="")
            print("")
                
            

class Board:
    def __init__(self):
        self.boards = [HomeBoard(), HomeBoard()] # white=0, black=1
        
    def display(self):
        print("\n     A     B     C     D         E     F     G     H")
        self.boards[0].display("white")
        print(" ______________________________________________________")
        self.boards[1].display("black")




class GameLogic:
    def __init__(self):
        self.board = Board()
        self.player = 1; # white=0, black=1
        
    def parseInput(self, row, col):

        try:
            int_row = int(row)
        except ValueError:
            return None, None, None
        
        if(int_row > 0 and int_row < 5) :
            row_index = int_row - 1
        else:
            return None, None, None
        
        if(col == 'A' or col == 'a'):
            return row_index, 0, 0
        elif(col == 'B' or col == 'b'):
            return row_index, 1, 0
        elif(col == 'C' or col == 'c'):
            return row_index, 2, 0
        elif(col == 'D' or col == 'd'):
            return row_index, 3, 0
        elif(col == 'E' or col == 'e'):
            return row_index, 0, 1
        elif(col == 'F' or col == 'f'):
            return row_index, 1, 1
        elif(col == 'G' or col == 'g'):
            return row_index, 2, 1
        elif(col == 'H' or col == 'h'):
            return row_index, 3, 1   
        else:
            print('a')
            return None, None, None
        
        
    def passiveMove(self) :     
        while(True):
            print("\nPassive Move1:", end="")
            row_from, col_from = input("Select a piece from your homeboard (<row> <column>): ").split()
            row_index, col_index, side = self.parseInput(row_from, col_from)
            
            if(row_index is None or col_index is None or side is None):
                print("INVALID INPUT")
                continue
            print(self.board.boards[0].color_boards[side][row_index][col_index])
            print(self.board.boards[1].color_boards[side][row_index][col_index])
            if((self.player == 0 and self.board.boards[0].color_boards[side][row_index][col_index] == 'W') or
               (self.player == 1 and self.board.boards[1].color_boards[side][row_index][col_index] == 'B')):
                break
                print(row_index, col_index, side)
                return row_index, col_index, side
            else:
                print("CHOOSE A PIECE OF YOUR COLOR")
            
            
            
        
    def turn(self):
        self.board.display()
        if(self.player): 
            print("\nBlack player's turn:") 
        else: 
            print("\nWhite player's turn:")
            
            
        x,y,z = self.passiveMove()
        
        print("INPUT WAS: ")
        print(x)
        
        
    

def main() :
    game = GameLogic()
    game.turn()
    
main()