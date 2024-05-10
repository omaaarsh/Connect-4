import random
ROW_COUNT = 6
COLUMN_COUNT = 7
GAME_OVER=0
SQUARE_SIZE=100
WIDTH=COLUMN_COUNT*SQUARE_SIZE
HEIGHT=(ROW_COUNT+1)*SQUARE_SIZE
SIZE=(WIDTH,HEIGHT)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
RADIUS = int(SQUARE_SIZE/2 - 5)
PLAYER=0
AI=1
TURN=random.randint(PLAYER,AI)
WINDOW_LENGTH=4
PLAYER_PIECE=1
AI_PIECE=2
EMPTY=0
# import pygame
# import sys

# # Initialize Pygame
# pygame.init()
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Music Player")
# pygame.mixer.init()
# pygame.mixer.music.load("/Users/compumagic/Downloads/connect 4/in_the_quiet_of_the_night_-_Quietness47.mp3")

# # Wait for the music to finish playing
# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)

# pygame.quit()
# sys.exit()