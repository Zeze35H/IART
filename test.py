import timeit
import copy


def copyBoard(board):
    board_aux = []

    board_aux = []
    for row in range(4):
        row_aux = []
        for col in range(4):
            row_aux.append(board[row][col]) # add element
        board_aux.append(row_aux) # add row
        
    return board_aux                

def copyBoards(boards):
        
        result = []
        for homeboard in range(2):
            homeboard_aux  = []
            for board in range(2):
                board_aux = []
                for row in range(4):
                    row_aux = []
                    for col in range(4):
                        row_aux.append(boards[homeboard][board][row][col]) # add element
                    board_aux.append(row_aux) # add row
                homeboard_aux.append(board_aux) # add board
            result.append(homeboard_aux) # add homeboard
            
        return result                
                        

def main():
    
    boards = [[[['W', 'W', 'W', 'W'],
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
    
    board = [['W', 'W', 'W', 'W'],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             ['B', 'B', 'B', 'B']]
    
    board_string = "[[[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']],[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']]],[[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']],[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']]]]"
    
    # start_time1 = timeit.default_timer()
    # for i in range(230):
    #     for j in range(230):
    #             x = copy.deepcopy(boards)
    # elapsed = timeit.default_timer() - start_time1
    # print("DeepCopy Elapsed Time: ", elapsed)
    
    start_time2 = timeit.default_timer()
    for i in range(230):
        for j in range(230):
                x = copyBoards(boards)
    elapsed = timeit.default_timer() - start_time2
    print("1:4 CopyBoard Elapsed Time: ", elapsed)
    
    start_time4 = timeit.default_timer()
    for i in range(230):
        for j in range(230):
                for k in range(2):
                    x = copyBoard(board)
    elapsed = timeit.default_timer() - start_time4
    print("4:1 CopyBoard Elapsed Time: ", elapsed)
    
    # start_time3 = timeit.default_timer()
    # for i in range(230):
    #     for j in range(230):
    #         x = copy.copy(board_string)
    # elapsed = timeit.default_timer() - start_time3
    # print("String Copy Elapsed Time: ", elapsed)


main()
