import pygame
import numpy
from game_lib.SharedClasses import ConfirmButton, BackButton, CircuitButton, Tutorial Block
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH
from prisoner_dilemma.StartStage import Knob

    
class Officer():

    width = 400
    height = 300

    def __init__(self, pos):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/Alice_officer.png'),
                                            (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self.surface):
        surface.blit(self.image, self.rect.topleft)


class GBButton():

    #Set the default size of the buttons while assuming the Angle of each is settled as pi/2
    width = 75
    height = 50
    
    #text is for decide weither print Good or Bad
    def __init__(self, pos, angle, color, text=''):

        self.angle = angle
        #setting the ratio of size
        based on angle
        self.goodRatio = 2*(self.angle/180)
        self.badRatio = 2*(1-self.angle/180)
        self.color = color
        self.text = text
        
        font = pygame.font.SysFont('timesnewroman',30*self.Ratio)
        text = font.render(self.text, 1, (0,0,0))


    def draw(self, surface):
        if self.text == 'GOOD!'
            self.rect = pygame.Rect((0,0), outline,(self.goodRatio*self.width, self.goodRatio*self.height))
        elif self.text == 'BAD!':
            self.rect = pygame.Rect((0,0), outline,(self.badRatio*self.width, self.badRatio*self.height))


        self.rect.bottomleft = (pos[0]-self.width/2, pos[1]+self.height/2)
        surface.fill(pygame.Color(self.color), self.rect)
        surface.blit(text, (self.rect.center-text.get_width()/2, self.rect.center-text.get_height()/2))
        
            
class AliceStage:

    def __init__(self, data):

        self.data = data:

            self.screen = pygame.display.get_suface()
            self.screen_rect = self.screen.get_rect()
            self.clock = pygame.time.Clock()
            self.fps = FPS

            self.keys = pygame.key.get_pressed()

            self.dragged_k = None
            self.checked_cb = None

            cx, cy = self.screen_rect.center

            
            self.officer = Officer((2*cx/3, cy-150))
            
            self.Knobs = [Knob((50, cy/2-60),numpy.pi/2), #theta
                          Knob((50, cy/2+60),0)]          #phi  
            
            self.GBButtons = [GBButton((2*cx/3+75, cy+50),self.Knobs[0].angle, 'red', 'GOOD!'),
                              GBButton((cx-100, cy+50),self.Knobs[0].angle, 'blue', 'BAD!')]

            self.ConfirmButton = ConfirmButton()
            self.BackButton = BackButton()
            self.CircuitButton = CircuitButton()

            self.next_stage = False
            self.quit = False
            self.back = False
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
                draw(self.screen)

            self.officer.draw(self.screen)
            self.ConfirmButton.draw(self.screen)
            self.BackButton.draw(self.screen)
            self.CircuitButton.draw(self.screen)
            self.caption.draw(self.screen)

            pygame.display.update()


        def main_loop(self):

            while not (self.quit or self.next_stage or self.back or self.show_circuit):
                self.event_loop()


                k = self.Knobs[0]
                k.update_drag()

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
                    

            

            
                                   
