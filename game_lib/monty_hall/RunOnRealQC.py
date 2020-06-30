import pygame
from game_lib.SharedClasses import BackButton, CircuitButton
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH


class Message():
    width = 400
    height = 150

    def __init__(self, pos):
        self.text = pygame.font.SysFont('timesnewroman', 40).render(
            "Would you like to run on a real Quantum Computer?", True, pygame.Color("black"))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos

        self.clickable = False

    def draw(self, surface):
        surface.blit(self.text, self.text_rect.topleft)


class YesButton():
    width = 130
    height = 100

    def __init__(self):

        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/Yes_button.png'),
                                            (self.width, self.height))
        self.rect = self.image.get_rect()

        cx, cy = pygame.display.get_surface().get_rect().center
        self.rect.center = (cx - 100, cy * 7 / 5)

        self.click = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True

    def update_click(self):
        if self.click == True:
            self.click = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class NoButton():
    width = 130
    height = 100

    def __init__(self):

        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/No_button.png'),
                                            (self.width, self.height))
        self.rect = self.image.get_rect()

        cx, cy = pygame.display.get_surface().get_rect().center
        self.rect.center = (cx + 100, cy * 7 / 5)
        self.click = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True

    def update_click(self):
        if self.click == True:
            self.click = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class RunOnRealQC():
    def __init__(self, data):
        self.data = data

        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        cx, cy = self.screen_rect.center

        # display objects
        self.Message = Message((cx, cy))

        # buttons
        self.YesButton = YesButton()
        self.NoButton = NoButton()
        self.BackButton = BackButton()
        self.CircuitButton = CircuitButton()

        self.tutorial_on = False
        # self.TutorialBlocks = [TutorialBlock()]

        self.next_stage = False
        self.quit = False
        self.back = False
        self.show_circuit = False
        self.real_qc = None

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    self.YesButton.check_click(event.pos)
                    self.NoButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)

            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.keys = pygame.key.get_pressed()

    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))

        self.YesButton.draw(self.screen)
        self.Message.draw(self.screen)

        self.NoButton.draw(self.screen)
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)

        pygame.display.update()
        pygame.display.update()

    def main_loop(self):

        while not (self.quit or self.next_stage or self.back or self.show_circuit or self.real_qc != None):
            self.event_loop()

            if self.NoButton.click:
                self.NoButton.update_click()
                self.real_qc = False
            elif self.BackButton.click:
                self.BackButton.update_click()
                self.back = True
            elif self.CircuitButton.click:
                self.CircuitButton.update_click()
                self.show_circuit = True
            elif self.YesButton.click:
                self.YesButton.update_click()
                self.real_qc = True

            self.render()
            self.clock.tick(self.fps)
