import numpy as np
from constants import *
import pygame
import os
import sys
import math
import random
# intialize the pygame 
pygame.init()
#play music
pygame.mixer.init()
# Using a raw string
pygame.mixer.music.load("/Users/compumagic/Downloads/connect 4/in_the_quiet_of_the_night_-_Quietness47.mp3")
pygame.init()
#Clear screen
def ClearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
	
#Create the Board
def CreateBoard():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT)) #Make the board as an array 6*7 with 0
	return board
board = CreateBoard()

# Drop pieces
def DropPiece(board, row, col, piece): # take the kind of piece and the position and board
	board[row][col] = piece

# Check validation 
def IsValidLocation(board, col):
	return board[ROW_COUNT-1][col] == 0 # if the position is 0 it means that means that no piece here

# Get the next row 
def GetNextOpenRow(board, col): # it will return the number of row to drop the piece 
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

# print the Board 
def PrintBoard(board):
	print(np.flip(board, 0)) # flip will reverse the order of elements in an array 

# winner check
def CheckWinner(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
			
# Drow the Board
def DrawBoard(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
	#Draw the circles
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
	pygame.display.update()
# evaluate the board
def EvaluateWindow(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4
	return score
#get score 
def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += EvaluateWindow(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += EvaluateWindow(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += EvaluateWindow(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += EvaluateWindow(window, piece)
	return score

# Get valid position of columns
def GetValidLocations(board):
	validLocations = []
	for col in range(COLUMN_COUNT):
		if IsValidLocation(board, col):
			validLocations.append(col)
	return validLocations
		
#return the best column that make the best move
def PickBestMove(Board,piece):
	validLocations=GetValidLocations(board)
	bestScore=0
	bestColumn =random.choice(validLocations)
	for col in validLocations:
		row=GetNextOpenRow(Board, col)
		tembBoard=board.copy()
		DropPiece(tembBoard,row,col,piece)
		score=score_position(tembBoard,piece)
		if score>bestScore:
			bestScore=score
			bestColumn=col
			print(bestScore)
	return bestColumn

# like is the game end 
def IsTerminalNode(board):
	return CheckWinner(board, PLAYER_PIECE) or CheckWinner(board, AI_PIECE) or len(GetValidLocations(board)) == 0

#MiniMax+Alpha+Beta+Pruning 😘
def MiniMax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = GetValidLocations(board)
	is_terminal = IsTerminalNode(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if CheckWinner(board, AI_PIECE):
				return (None, 100000000000000)
			elif CheckWinner(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = GetNextOpenRow(board, col)
			b_copy = board.copy()
			DropPiece(b_copy, row, col, AI_PIECE)
			new_score = MiniMax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = GetNextOpenRow(board, col)
			b_copy = board.copy()
			DropPiece(b_copy, row, col, PLAYER_PIECE)
			new_score = MiniMax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
# Make Screen
screen=pygame.display.set_mode(SIZE)
# Set caption for screen
pygame.display.set_caption("Connect4")

DrawBoard(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
while not GAME_OVER:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            if TURN == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARE_SIZE))
            # Ask for Player 1 Input
            if TURN == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if IsValidLocation(board, col):
                    row = GetNextOpenRow(board, col)
                    DropPiece(board, row, col, PLAYER_PIECE)

                    if CheckWinner(board, 1):
                        label = myfont.render("  you win!!", 1, RED)
                        screen.blit(label, (40,10))
                        GAME_OVER = True
                    PrintBoard(board)
                    DrawBoard(board)
                    # Change the turn
                    TURN += 1
                    TURN = TURN % 2
                    if GAME_OVER:
                        pygame.time.wait(3000)

        # Ask for AI Input
        if TURN == AI and not GAME_OVER:
            pygame.time.wait(500)
            col, minimax_score = MiniMax(board, 5, -math.inf, math.inf, True)

            if IsValidLocation(board, col):
                row = GetNextOpenRow(board, col)
                DropPiece(board, row, col, AI_PIECE)

                if CheckWinner(board, 2):
                    label = myfont.render("   AI wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    GAME_OVER = True

                PrintBoard(board)
                pygame.display.update()  # Update display after AI move
                DrawBoard(board)
                # Change the turn
                TURN += 1
                TURN = TURN % 2

                if GAME_OVER:
                    pygame.time.wait(3000)
