import copy

"""
Regions are indetified by their upper-left cells, regions are 3x3 sub-matrices
"""
region_mapper = [ (0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6) ]

"""
Validates board dimensions
"""
def validate_board(board):
    N = len(board)

    if N != 9:
        raise Exception("A valid Sudoko board must have 9 rows")

    for i in range(9):
        if len(board[i]) != 9:
            raise Exception("A valid Sudoku board must have 8 columns")
    M = 9
    
"""
Recursive brute force solver: For each cell, try all possible available values for itself until find a valid solution
"""

def solve(board, x, y, rows, cols):
    if x > 8:
        return board
    elif y > 8:
        return solve(board, x + 1, 0, rows, cols)
    else:        
        if board[x][y] != 0:
            return solve(board, x, y + 1, rows, cols)
        else:
            valid = [ True for _ in range(10) ]

            for i in range(1, 10):
                if rows[x][i]:
                    valid[i] = False
                if cols[y][i]:
                    valid[i] = False

            for _ in range(9):
                inside = False
                
                for i in range(3):
                    for j in range(3):
                        xi = region_mapper[_][0] + i
                        yi = region_mapper[_][1] + j

                        if xi == x and yi == y:
                            inside = True
                if inside:
                    for i in range(3):
                        for j in range(3):
                            xi = region_mapper[_][0] + i
                            yi = region_mapper[_][1] + j

                            if board[xi][yi] != 0:
                                valid[board[xi][yi]] = False

            for i in range(1, 10):
                if valid[i]:
                    next_rows = copy.deepcopy(rows)
                    next_cols = copy.deepcopy(cols)

                    next_board = copy.deepcopy(board)
                    
                    next_rows[x][i] = True
                    next_cols[y][i] = True

                    next_board[x][y] = i

                    check_board = solve(next_board, x, y + 1, next_rows, next_cols)

                    if check_board != False:
                        return check_board
                    
            return False;                    

def do(board):
    rows = [ [ False for i in range(10) ] for _ in range(9) ]
    cols = [ [ False for i in range(10) ] for _ in range(9) ]

    for i in range(9):
        for j in range(9):
            rows[i][board[i][j]] = True
            cols[j][board[i][j]] = True

    return solve(board, 0, 0, rows, cols)
    
def read_board():
    board = []

    for i in range(9):
        board.append(list(input()))

        if board[i][-1] == '\r':
            del board[i][-1]

        if len(board[i]) != 9:
            print(board[i])
            raise Exception("Number of elements in row {0} is {1}, which is different from 9 from standard Sudoku Game".format(i, len(board[i])))

        for j in range(9):
            if board[i][j] == '.':
                board[i][j] = 0
            else:
                board[i][j] = int(board[i][j])
    return board

if __name__ == "__main__":
    board = read_board()

    solved = do(board)

    for i in range(9):
        print(solved[i])
        
