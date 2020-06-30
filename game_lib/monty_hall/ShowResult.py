import pygame
from game_lib.SharedClasses import BackButton, CircuitButton, ConfirmButton
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH


class Celebration():
    width = 400
    height = 200

    def __init__(self, pos, data):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/celebration.png'),
                                            (self.width, self.height))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = pos

        if data['Measurement'] == 0:
            self.text = pygame.font.SysFont('timesnewroman', 50).render(
                "Alice Wins!", True, pygame.Color("black"))
        elif data['Measurement'] == 1:
            self.text = pygame.font.SysFont('timesnewroman', 50).render(
                "Bob Wins!", True, pygame.Color("black"))
        else:
            raise ValueError('Not a possible measurement result')

        self.text_rect = self.text.get_rect()
        self.text_rect.center = (pos[0], pos[1] + 100)

        self.clickable = False

    def draw(self, surface):
        surface.blit(self.image, self.image_rect.topleft)
        surface.blit(self.text, self.text_rect.topleft)


class Message():
    width = 400
    height = 150

    def __init__(self, pos, data):
        font = pygame.font.SysFont('timesnewroman', 30)
        self.text0 = font.render(f"Measurement result is {data['Measurement']}", True, pygame.Color("blue"))
        self.text1 = font.render('Approximate win rates:', True, pygame.Color("blue"))
        self.text2 = font.render(f"Alice: {data['WinRate'][0]}; Bob: {data['WinRate'][1]}", True, pygame.Color("blue"))
        self.text0_rect = self.text0.get_rect()
        self.text0_rect.center = (pos[0], pos[1]-30)
        self.text1_rect = self.text1.get_rect()
        self.text1_rect.center = pos
        self.text2_rect = self.text2.get_rect()
        self.text2_rect.center = (pos[0], pos[1]+30)

        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/frame.png'),
                                            (self.width, self.height))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = pos

    def draw(self, surface):
        surface.blit(self.text0, self.text0_rect.topleft)
        surface.blit(self.text1, self.text1_rect.topleft)
        surface.blit(self.text2, self.text2_rect.topleft)
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
            (cx, Celebration.height/2), self.data)
        self.Message = Message((cx, cy + Message.height/4), self.data)

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
