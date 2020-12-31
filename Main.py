from chess import *
import time

chessBoard = Board()


def getMove(board):

    lowerCase = 'qrbnp'
    upperCase = 'QRBNP'

    whiteMove = False
    blackMove = False
    try:
        if str(board.piece_at(globals()[str(str(list(board.legal_moves)[0])[:2]).upper()])) in upperCase:
            whiteMove = True
            blackMove = False
        else:
            whiteMove = False
            blackMove = True
    except:
        board.pop()
        if board.piece_at(globals()[str(str(list(board.legal_moves)[0])[:2]).upper()]) in upperCase:
            whiteMove = False
            blackMove = True
        else:
            whiteMove = True
            blackMove = False
    return whiteMove, blackMove


def getSquares():
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    squares = []
    for i in range(1, 9):
        for j in range(8):
            squares.append(alpha[j].upper() + str(i))

    return squares


def copyBoard(board):
    fen = board.fen()
    clone = Board()
    clone.set_fen(fen)
    return clone


def Evaluate(board):
    def piece(square):
        return str(board.piece_at(globals()[square.upper()]))

    blackValue = 0
    whiteValue = 0

    pieceValues = {"q": 9, "r": 5, "n": 3, "b": 3, "p": 1}
    pieceTypes = list(pieceValues.keys())

    lowerCase = 'qrbnp'
    upperCase = 'QRBNP'

    for pieceType in pieceTypes:
        pieceValues[pieceType.upper()] = pieceValues[pieceType]

    # Getting currentMove
    whiteMove, blackMove = getMove(board)
    # Getting squares
    squares = getSquares()

    # Adding piece values to board value
    for square in squares:
        if (piece(square) in upperCase):
            whiteValue += pieceValues[piece(square)]

        if (piece(square) in lowerCase):
            blackValue += pieceValues[piece(square)]

    # Adding possible moves to board value
    if (whiteMove):
        whiteValue += len(list(board.legal_moves))

        clone = copyBoard(board)
        moveLengths = []

        for move in list(clone.legal_moves):
            clone.push_uci(str(move))
            moveLengths.append(len(list(clone.legal_moves)))
            clone = copyBoard(board)

        averageLength = int(sum(moveLengths) / len(moveLengths))
        blackValue += averageLength

    else:
        blackValue += len(list(board.legal_moves))

        clone = copyBoard(board)
        moveLengths = []

        for move in list(clone.legal_moves):
            clone.push_uci(str(move))
            moveLengths.append(len(list(clone.legal_moves)))
            clone = copyBoard(board)

        averageLength = int(sum(moveLengths) / len(moveLengths))
        whiteValue += averageLength

    # Subtracting from board value if in check
    if (whiteMove and board.is_check()):
        whiteValue -= 10
        blackValue += 10
    elif (blackMove and board.is_check()):
        blackValue -= 10
        whiteValue += 10

    # Adding to board value if check-mate
    if (whiteMove and board.is_checkmate()):
        blackValue += 10000
        whiteValue -= 10000
    elif (blackMove and board.is_checkmate()):
        whiteMove += 10000
        blackMove -= 10000

    # Adding the value of pieces threatened
    attackValue = 0
    for move in list(board.legal_moves):
        if (board.is_capture(move)):
            attackValue += pieceValues[piece(str(move)[2:])]

    if (whiteMove): whiteValue += attackValue
    if (blackMove): blackValue += attackValue

    #Subtracting from board value if pieces threatened
    testBoard = copyBoard(board)
    enemyCaptureMoves = []

    for move in list(testBoard.legal_moves):
        testBoard.push_uci(str(move))
        for respondingMove in list(testBoard.legal_moves):
            if(testBoard.is_capture(respondingMove)):
                enemyCaptureMoves.append(str(respondingMove))
        testBoard = copyBoard(board)

    numberOfEnemyCaptureMoves = {}

    for captureMove in enemyCaptureMoves:
        try:
            numberOfEnemyCaptureMoves[captureMove] += 1
        except:
            numberOfEnemyCaptureMoves[captureMove] = 1

    reuccuringEnemyCaptureMoves = []

    for captureMove in numberOfEnemyCaptureMoves:
        if(numberOfEnemyCaptureMoves[captureMove] > 4):
            reuccuringEnemyCaptureMoves.append(captureMove)

    threatenedValue = 0

    for move in list(reuccuringEnemyCaptureMoves):
        if(piece(str(move)[2:]).lower() == 'q'):
            print("QUEEN THREATENED")
        threatenedValue += pieceValues[piece(str(move)[2:])]*10

    if (whiteMove): whiteValue -= threatenedValue
    if (blackMove): blackValue -= threatenedValue

    return whiteValue, blackValue


def getMoveFromBoard(board):
    evaluations = {}

    whiteValues = []
    blackValues = []
    testBoard = copyBoard(board)

    print(list(testBoard.pseudo_legal_moves))

    for move in list(board.legal_moves):
        testBoard.push_uci(str(move))
        evaluations[str(move)] = [Evaluate(testBoard)[0], Evaluate(testBoard)[1]]
        testBoard = copyBoard(board)

    for move in list(board.legal_moves):
        whiteValues.append(evaluations[str(move)][0])
        blackValues.append(evaluations[str(move)][1])

    moveToMake = None
    if (getMove(board)[0]):
        for move in list(board.legal_moves):
            if (evaluations[str(move)][0] == max(whiteValues)):
                moveToMake = str(move)
                break
    if (getMove(board)[1]):
        for move in list(board.legal_moves):
            if (evaluations[str(move)][1] == max(blackValues)):
                moveToMake = str(move)
                break

    return moveToMake

while 1:
    move = input("Move : ")
    chessBoard.push_uci(move)
    aiMove = getMoveFromBoard(chessBoard)
    print("AI move : " + aiMove)
    chessBoard.push_uci(aiMove)
