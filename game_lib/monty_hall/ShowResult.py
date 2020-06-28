import pygame
from game_lib.SharedClasses import BackButton, CircuitButton, ConfirmButton
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH


class Celebration():
    width = 400
    height = 200

    def __init__(self, pos, expected_value):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/celebration.png'),
                                            (self.width, self.height))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = pos

        if expected_value < 0.5:
            self.text = pygame.font.SysFont('timesnewroman', 50).render(
                "Alice Wins!", True, pygame.Color("black"))
        else:
            self.text = pygame.font.SysFont('timesnewroman', 50).render(
                "Bob Wins!", True, pygame.Color("black"))

        self.text_rect = self.text.get_rect()
        self.text_rect.center = (pos[0], pos[1] + 100)

        self.clickable = False

    def draw(self, surface):
        surface.blit(self.image, self.image_rect.topleft)
        surface.blit(self.text, self.text_rect.topleft)


class Message():
    width = 400
    height = 150

    def __init__(self, pos, expected_value):
        self.text = pygame.font.SysFont('timesnewroman', 30).render(
            "Expected value is {}".format(expected_value), True, pygame.Color("blue"))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos

        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/frame.png'),
                                            (self.width, self.height))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = pos

        self.clickable = False

    def draw(self, surface):
        surface.blit(self.text, self.text_rect.topleft)
        surface.blit(self.image, self.image_rect.topleft)


class ShowResult():
    def __init__(self, data):
        self.data = data

        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        cx, cy = self.screen_rect.center

        # display objects
        self.Celebration = Celebration(
            (cx, Celebration.height/2), self.data['ExpectedValue'])
        self.Message = Message((cx, cy + Message.height/4),
                               self.data['ExpectedValue'])

        # buttons
        self.ConfirmButton = ConfirmButton()
        self.BackButton = BackButton()
        self.CircuitButton = CircuitButton()

        self.tutorial_on = False
        # self.TutorialBlocks = [TutorialBlock()]

        self.next_stage = False
        self.quit = False
        self.back = False
        self.show_circuit = False

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    self.ConfirmButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)

            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.keys = pygame.key.get_pressed()

    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))

        self.Celebration.draw(self.screen)
        self.Message.draw(self.screen)

        self.ConfirmButton.draw(self.screen)
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)

        pygame.display.update()
        pygame.display.update()

    def main_loop(self):

        while not (self.quit or self.next_stage or self.back or self.show_circuit):
            self.event_loop()

            if self.ConfirmButton.click:
                self.ConfirmButton.update_click()
                self.next_stage = True
            elif self.BackButton.click:
                self.BackButton.update_click()
                self.back = True
            elif self.CircuitButton.click:
                self.CircuitButton.update_click()
                self.show_circuit = True

            self.render()
            self.clock.tick(self.fps)
