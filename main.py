import pygame
import os
import sys
from game_lib.Menu import Menu
from game_lib.parameters import CAPTION, SCREEN_SIZE
#from pygame import DOUBLEBUF, HWSURFACE, FULLSCREEN


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption(CAPTION)
#flags = DOUBLEBUF | HWSURFACE | FULLSCREEN
#pygame.display.set_mode(SCREEN_SIZE, flags)
pygame.display.set_mode(SCREEN_SIZE)
#pygame.mixer.music.load("data/mightbebgm.mp3") 
#pygame.mixer.music.play(-1, 0.0)
Menu().main_loop()
pygame.quit()
sys.exit()
