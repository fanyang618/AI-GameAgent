# K in a row playing algorithm

from random import randint, choice
import time
import copy

#game info
winK = 0
mySide = ''
oppo = ''
#board info
length = 0
width = 0
forbid_square = []
zobrist_table = []
move_history = {}


#pregame info setup                
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    global winK, mySide, oppo, length, width, forbid_square, vertical, horizontal, left_low_diag, right_low_diag
    board = initial_state[0]
    #game info input
    winK = k
    mySide = what_side_I_play
    oppo = opponent_nickname
    #board dimension
    length = len(board)
    width = len(board[0])
    #forbidden_squares
    for row in range(length):
        for col in range(width):
            if board[row][col] == '-':
                forbid_square.append((row, col))
    #initialize zobrist hash table
    zinit()
    
    return 'OK'

#find best move and give response
def makeMove(currentState, currentMak, timeLimit=10000):
    global length, width, mySide, winK
    bragList = ["I always knew you were stupid", "Wanna try gain? You'll lose anyway", "I love the look when you try, it's cute"]
    warningList = ["careful, idiot.", "Think cautiously, I know it's hard for you", "I think I should be nice to dumb dumb, open your eyes"]
    tauntList = ["meh, that move was ok", "this game seems easy", "Hurry up, I'm falling asleep!"]

    startTime = time.time()
    calculation = minimax(currentState, timeLimit, startTime, 4)
    nextState = calculation[1]
    evaluation = calculation[0]
    insertRow = 0
    insertCol = 0
    response = ''
    if evaluation > pow(10, winK - 2):
        response = choice(bragList)
    elif (evaluation <= pow(10, winK - 2) and evaluation > pow(10, winK - 3)):
        response = choice(warningList)
    elif (evaluation <= pow(10, winK - 3)):
        response = choice(tauntList)
        
    for row in range(length):
        for col in range(width):
            if currentState[0][row][col] != nextState[0][row][col]:
                insertRow = row
                insertCol = col
                break
            else :
                continue
            break
        insert = [insertRow, insertCol]
        result = [[insert, nextState], response]
    return result

def minimax(state, timeLimit, startTime, plyLeft, a, b):
    global mySide
    # return a result when timelimit is hit
    if time.time() - startTime >= 0.7 * timeLimit:
        return [staticEval(state), state]
    nextState = []
    currentSide = state[1]
    if plyLeft == 0:
        return [staticEval(state), state]
    if currentSide == mySide:
        bound = -99999999
    else :
        bound = 99999999
    for eachState in successors(state, currentSide):
        #board_id = zhash(eachState[0])
        result = minimax(eachState, timeLimit, startTime, plyLeft - 1)
        #move_history[board_id] = result
        updateVal = result[0]
        if (currentSide == mySide and updateVal > bound) or (currentSide == switch(mySide) and updateVal < bound):
            bound = updateVal
            nextState = eachState
        # prune the branch if current search branch exceeded alpha-beta bounds
        if (currentSide == mySide and updateVal >= b) or (currentSide == switch(mySide) and updateVal <= a):
            break
        if (currentSide == mySide):
            a = max(a, updateVal)
        else:
            b = min(b, updateVal)
    return [bound, nextState]

#return a list of all the successors of the current State
def successors(state, currentSide):
    global width, length
    board = state[0]
    successor = []
    for row in range(length):
        for col in range(width):
            if board[row][col] == ' ':
                newBoard = copy.deepcopy(board)
                newBoard[row][col] = currentSide
                newState = [newBoard, switch(currentSide)]
                successor.append(newState)
    return successor

#return the opponent's symbol
def switch(side):
    if side == "X":
        return "O"
    else:
        return "X"

def staticEval(state):
    global winK
    evaluation = 0
    for pieceCount in range (2, winK + 1):
        board = state[0]
        xrows = scanBoard(board, 'X', pieceCount)
        orows = scanBoard(board, 'O', pieceCount)
        if pieceCount == winK and xrows > 0:
            return float('inf')
        elif pieceCount == winK and orows > 0:
            return float('-inf')
        else:
            evaluation = evaluation + pow(10, pieceCount) * (xrows - orows)
    return evaluation
      
def scanBoard(board, side, pieceCount):
    global length, width
    evaluation = 0
    # check diagonal
    for row in range(length):
        for col in range(width):
            backslash = [(row + i, col + i) for i in range(pieceCount)]
            slash = [(row + i, col - i) for i in range(pieceCount)]
            check_backslash = True
            try:
                for square in slash:
                    if board[square[0]][square[1]] != side:
                        check_backslash = False
                        break
                try:
                    if board[square[0] + 1][square[1] + 1] == side or board[row - 1][col - 1] == side:
                        check_backslash = False
                except IndexError:
                    pass
            except IndexError:
                check_backslash = False
            if check_backslash:
                evaluation += 1
            check_slash = True
            try:
                for square in slash:
                    if board[square[0]][square[1]] != side:
                        check_slash = False
                        break
                try:
                    if board[square[0] + 1][square[1] - 1] == side or board[row - 1][col + 1] == side:
                        check_slash = False
                except IndexError:
                    pass
            except IndexError:
                check_slash = False
            if check_slash:
                evaluation += 1

    #check horizontal
    for row in range(length):
        for col in range (width - pieceCount + 1):
            if board[row][col] == side:
                check_horizontal = True
                try:
                    for nextCol in range(col + 1, col + pieceCount):
                        if board[row][nextCol] != side:
                            check_horizontal = False
                            break
                    if check_horizontal:
                        evaluation += 1
                except IndexError:
                    pass

    #check vertical
    for col in range(width):
        for row in range(length - pieceCount + 1):
            if board[row][col] == side:
                check_vertical = True
                try :
                    for nextRow in range(row + 1, row + pieceCount):
                        if board[nextRow][col] != side:
                            check_vertical = False
                            break
                    if check_vertical:                        evaluation += 1
                except IndexError:
                    pass
    return evaluation

def introduce():
    return 'Hi, my name is Aragaki Yui!\n' + 'Created by: Fan Yang(ID: 1430535)\n' + 'I will try to be as nice as I could be as long as you are not stupid :)'

def nickname():
    return 'Gakki~'

    #zobrist hash table initiation
def zinit():
    global zobrist_table, length, width
    zobrist_table = [[[0] * 2] * width] * length
    for row in range(length):
        for col in range(width):
            for k in range(2):
                zobrist_table[row][col][k] = randint(0, 4294967296)

#zobrist hashing
def zhash(board):
    global zobrist_table, length, width, forbid_square
    val = 0
    for row in range(length):
        for col in range(width):
            if (row, col) not in forbid_square:
                piece = None
                if board[row][col] == 'X':
                    piece = 0
                if board[row][col] == 'O':
                    piece = 1
                if piece != None:
                    val ^= zobrist_table[row][col][piece]
    return val
