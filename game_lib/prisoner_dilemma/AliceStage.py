import pygame
import numpy as np
from game_lib.SharedClasses import ConfirmButton, BackButton, CircuitButton, TutorialBlock, Knob
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH

class Caption:
    width = 800
    height = 200

    def __init__(self, pos):
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        font = pygame.font.SysFont('timesnewroman', 50)
        self.text = font.render('Is Bob...?', True, pygame.Color("black"))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos

    def draw(self, surface):
        surface.blit(self.text, self.text_rect)

class Theta():

    width = 50
    height = 50
    def __init__(self, pos):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/theta.png'),
                                            (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Phi():
    width = 40
    height = 40
    def __init__(self, pos):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/phi.png'),
                                            (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Officer():
    width = 400
    height = 450

    def __init__(self, pos):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/AliceOfficer.png'),
                                            (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class GBButton():
    # Set the default size of the buttons while assuming the Angle of each is settled as pi/2
    width = 75
    height = 40

    # text is for decide weither print Good or Bad
    def __init__(self, pos, angle, color, text=''):

        self.angle = angle
        # setting the ratio of size
        # based on angle
        # self.goodRatio = 2*(self.angle/180)
        # self.badRatio = 2*(1-self.angle/180)

        self.update_ratio(self.angle)
        self.color = color
        self.text = text
        self.pos = pos

        #if self.text == 'GOOD!':
        #    self.font = pygame.font.SysFont('timesnewroman', int(30))
         #   self.text0 = self.font.render(self.text, True, pygame.Color("black"))
        #elif self.text == 'BAD!':
      #      self.font = pygame.font.SysFont('timesnewroman', int(30))
     #       self.text0 = self.font.render(self.text, True, pygame.Color("black"))
     #   else:
     #       raise ValueError('text must be "GOOD!" or "BAD!"')

    def update_ratio(self,angle):
        self.angle = angle
        self.ratio = [ 2*(self.angle/np.pi), (2*(1 - self.angle/np.pi))]

    def draw(self, surface):
        if self.text == 'GOOD!':
            self.rect = pygame.Rect((0, 0), (self.ratio[0] * self.width, self.ratio[0] * self.height))
            self.font = pygame.font.SysFont('timesnewroman', int(25*self.ratio[0]))
            self.text0 = self.font.render(self.text, True, pygame.Color("black"))

        elif self.text == 'BAD!':
            self.rect = pygame.Rect((0, 0), (self.ratio[1] * self.width, self.ratio[1] * self.height))
            self.font = pygame.font.SysFont('timesnewroman', int(30*self.ratio[1]))
            self.text0 = self.font.render(self.text, True, pygame.Color("black"))
        else:
            raise ValueError('text must be "GOOD!" or "BAD!"')

        self.rect.bottomleft = (self.pos[0] - self.width / 2, self.pos[1] + self.height / 2)
        surface.fill(pygame.Color(self.color), self.rect)
        surface.blit(self.text0, (
        self.rect.bottomleft[0], self.rect.bottomleft[1] - self.text0.get_height()))


class AliceStage:

    def __init__(self, data):

        self.data = data

        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        self.dragged_k = None
        self.checked_cb = None

        cx, cy = self.screen_rect.center

        self.Officer = Officer((5*cx / 3, cy - 100))
        self.Phi = Phi((100, cy + 60))
        self.Theta = Theta((100, cy - 60))
        self.caption = Caption((cx, 0.5*cy))

        self.Knobs = [Knob((50, cy - 60), np.pi/2),  # theta
                      Knob((50, cy + 60), 0)]  # phi

        self.GBButtons = [GBButton((cx + 75, cy + 150), self.Knobs[0].angle, 'red', 'GOOD!'),
                          GBButton((cx - 100, cy + 150), self.Knobs[0].angle, 'blue', 'BAD!')]

        self.ConfirmButton = ConfirmButton()
        self.BackButton = BackButton()
        self.CircuitButton = CircuitButton()

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
                    for k in self.Knobs:
                        k.check_click(event.pos)
                        if k.click == True:
                            self.dragged_k = k
                            break

                    self.ConfirmButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)


            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for k in self.Knobs:
                        if k.click:
                            k.click = False
                            self.dragged_k = None
                            break

            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.keys = pygame.key.get_pressed()

    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))

        for k in self.Knobs:
            k.draw(self.screen)

        for i in self.GBButtons:
            i.draw(self.screen)

        self.Officer.draw(self.screen)
        self.Theta.draw(self.screen)
        self.Phi.draw(self.screen)
        self.ConfirmButton.draw(self.screen)
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)
        self.caption.draw(self.screen)

        pygame.display.update()

    def main_loop(self):

        while not (self.quit or self.next_stage or self.back or self.show_circuit):
            self.event_loop()

            for k in range(2):
                print(self.Knobs[k].angle)
                self.Knobs[k].update_drag()

            for i in range(2):
                self.GBButtons[i].update_ratio(self.Knobs[0].angle)



            self.phi = (self.Knobs[1].angle) * np.pi / 180
            self.theta = (self.Knobs[0].angle) * np.pi / 180

            self.data['UA'] = np.array([[np.exp(self.phi * 1j) * np.cos(self.theta / 2), -(np.sin(self.theta / 2))],
                                        [np.sin(self.theta / 2), np.exp(-self.phi * 1j) * np.cos(self.theta / 2)]])

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

            

            
                                   
