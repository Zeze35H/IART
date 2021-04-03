import timeit
import copy
import numpy


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
    
   
    board1 = [['W', 'W', 'W', 'W'],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             ['B', 'B', 'B', 'B']]
    
    board2 = [['W', 'W', 'W', 'W'],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             ['B', 'B', 'B', 'B']]
    board3 = [['W', 'W', 'W', 'W'],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             ['B', 'B', 'B', 'B']]
    board4 = [['W', 'W', 'W', 'W'],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             ['B', 'B', 'B', 'B']]
    
    array = numpy.array([[[['W', 'W', 'W', 'W'],
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
                  ['B', 'B', 'B', 'B']]]])
    
    
    arei = numpy.array([['W', 'W', 'W', 'W'],
                  [' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' '],
                  ['B', 'B', 'B', 'B']])

    
    # board_string = "[[[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']],[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']]],[[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']],[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']]]]"
    

    # start_time2 = timeit.default_timer()
    # for i in range(400000):
    #     x = copyBoards(boards)
    # elapsed = timeit.default_timer() - start_time2
    # print("1:4 CopyBoard Elapsed Time: ", elapsed)
    
    # start_time4 = timeit.default_timer()
    # for i in range(400000):
    #     for q in range(4):
    #         x = copyBoard(board1)            
    # elapsed = timeit.default_timer() - start_time4
    # print("4:1 CopyBoard Elapsed Time: ", elapsed)
    
    # start_time6 = timeit.default_timer()
    # for i in range(400000):
    #     x = np.copy(array)            
    # elapsed = timeit.default_timer() - start_time6
    # print("4:1 CopyBoard Elapsed Time: ", elapsed)
    
    # start_time8 = timeit.default_timer()
    # for i in range(400000):
    #     for q in range(4):
    #         x = np.copy(arei)            
    # elapsed = timeit.default_timer() - start_time8
    # print("4:1 CopyBoard Elapsed Time: ", elapsed)
    
    
    start_time1 = timeit.default_timer()
    a = []
    
    for i in range(5000):
        a.append(i)
    
    for x in a:
        b = 1 + 1
        
    elapsed = timeit.default_timer() - start_time1
    print("normal: ", elapsed)
    
    
    
    start_time2 = timeit.default_timer()
    a = numpy.array([])
    
    for i in range(5000):
        numpy.append(a,i)
    
    for x in a:
        b = 1 + 1
        
    elapsed = timeit.default_timer() - start_time2
    print("numpy: ", elapsed)
    
    
    



main()
