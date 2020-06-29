import pygame
import qiskit
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import gc
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH
from game_lib.SharedClasses import BackButton, CircuitButton
from game_lib.prisoner_dilemma.StartStage import StartStage
from game_lib.prisoner_dilemma.AliceStage import AliceStage
from numpy import array, arctan, sqrt, pi
from copy import deepcopy


class PrisonerDilemma:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        self.data = {'J': array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]),
                     'UA': array([[1,0],[0,1]])}

        self.stages = [StartStage,
                       AliceStage,
                       # AliceDecides,
                       # ShowResult
                       ]

        self.stage_index = 0

        self.quit = False
        self.back = False

        cx, cy = self.screen_rect.center
        # self.CircuitDisplay = CircuitDisplay(self.data)

        self.BackButton = BackButton()
        self.CircuitButton = CircuitButton()

    def event_loop(self):
        """
        This is the event loop for the whole program.
        Regardless of the complexity of a program, there should never be a need
        to have more than one event loop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.keys = pygame.key.get_pressed()

    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))

        # self.CircuitDisplay.draw(self.screen)

        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)

        pygame.display.update()

    def main_loop(self):
        current_stage = None
        while not (self.quit or self.back):
            for k, v in self.data.items():
                print(k, v)
            print()
            if self.stages[self.stage_index] != type(current_stage):
                current_stage = self.stages[self.stage_index](self.data)
            current_stage.main_loop()
            if current_stage.next_stage == True:
                # self.update_circuit()
                self.stage_index += 1
                if self.stage_index == len(self.stages):
                    self.back = True
            elif current_stage.back == True:
                self.back = True
            elif current_stage.quit == True:
                self.quit = True
            elif current_stage.show_circuit == True:
                # self.update_circuit()
                while (current_stage.show_circuit and not (self.quit or self.back)):
                    self.event_loop()
                    if self.BackButton.click:
                        self.BackButton.update_click()
                        self.back = True
                    elif self.CircuitButton.click:
                        self.CircuitButton.update_click()
                        current_stage.show_circuit = False
                    self.render()
                    self.clock.tick(self.fps)
            else:
                raise ValueError('Stage quits without proceeding')
