import pygame
from game_lib.monty_hall.MontyHall import MontyHall
from game_lib.prisoner_dilemma.PrisonerDilemma import PrisonerDilemma
from game_lib.parameters import BACKGROUND_COLOR, FPS


class StartButton():

    # width = 100
    # height = 50

    def __init__(self, name, game_class, pos):

        self.text = pygame.font.SysFont('timesnewroman', 30).render(name, True, pygame.Color("black"))
        self.rect = self.text.get_rect()
        self.rect.center = pos
        self.game_class = game_class

        self.clickable = True
        self.click = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True

    def start_game(self):
        if self.click == True:
            self.click = False
            return self.game_class()

    def draw(self, surface):
        surface.blit(self.text, self.rect)


class Menu():

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        cx, cy = self.screen_rect.center
        self.StartButtons = [StartButton('Monty Hall', MontyHall, (cx, cy - 50)), 
                             StartButton('Prisoner Dilemma', PrisonerDilemma, (cx, cy))]

        self.quit = False

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for sb in self.StartButtons:
                        sb.check_click(event.pos)
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.keys = pygame.key.get_pressed()

    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))

        for sb in self.StartButtons:
            sb.draw(self.screen)

        pygame.display.update()

    def main_loop(self):

        while not self.quit:
            self.event_loop()

            for sb in self.StartButtons:
                if sb.click == True:
                    new_game = sb.start_game()
                    new_game.main_loop()
                    if new_game.quit == True:
                        self.quit = True
                    break

            else:
                self.render()
