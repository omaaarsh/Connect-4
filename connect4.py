import numpy as np
from constants import *
import pygame
import os
import sys
import math
# intialize the pygame 
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
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
	pygame.display.update()

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
            if TURN == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
            else: 
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARE_SIZE))
			
            # Ask for Player 1 Input
            if TURN == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if IsValidLocation(board, col):
                    row = GetNextOpenRow(board, col)
                    DropPiece(board, row, col, 1)

                    if CheckWinner(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        GAME_OVER = True

            # # Ask for Player 2 Input
            else:				
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if IsValidLocation(board, col):
                    row = GetNextOpenRow(board, col)
                    DropPiece(board, row, col, 2)

                    if CheckWinner(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        GAME_OVER = True

            PrintBoard(board)
            DrawBoard(board)

            TURN += 1
            TURN = TURN % 2

            if GAME_OVER:
                pygame.time.wait(3000)
