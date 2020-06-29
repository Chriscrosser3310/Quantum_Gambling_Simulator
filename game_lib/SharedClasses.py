import pygame
from game_lib.parameters import IMAGE_PATH
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import gc

class Door():
    
    width = 100
    height = 200   
    
    def __init__(self, pos):   
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/door.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class DoorBar():
    
    width = Door.width
    height = Door.height  
    
    def __init__(self, pos, prob):
        
        self.rect = pygame.Rect((0,0), (self.width, prob*self.height))
        self.rect.bottomleft = (pos[0] - self.width/2, pos[1] + self.height/2)
        
        self.prob = prob
        self.update_text("{:03.1f}%".format(100*self.prob)) # self.text
        
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.rect.centerx, self.rect.bottom- self.height - 20)
        
        self.clickable = True
        self.click = False
    
    
    def check_click(self, pos):
        if self.rect.left <= pos[0] and self.rect.right >= pos[0]:
            if self.rect.bottom - self.height <= pos[1] and self.rect.bottom >= pos[1]:
                self.click = True
                pygame.mouse.get_rel()
    
    
    def update_text(self, message):
        font = pygame.font.SysFont('timesnewroman', 30)
        self.text = font.render(message, True, pygame.Color("black"))
    
    
    def update_drag(self):
        if self.click:
            dh = pygame.mouse.get_rel()[1]
            original_h = self.rect.h
            self.rect.h -= dh
            
            if self.rect.h > self.height:
                self.rect.h = self.height
            
            elif self.rect.h < 0:
                self.rect.h = 0
            
            center_moved = self.rect.h - original_h 
            self.rect.center = (self.rect.center[0], self.rect.center[1] - center_moved)

            self.prob = self.rect.h/self.height
            self.update_text("{:03.1f}%".format(100*self.prob))
    
    
    def update_with_prob(self, prob):
        original_h = self.rect.h
        self.rect.h = 200*prob
        
        center_moved = self.rect.h - original_h
        self.rect.center = (self.rect.center[0], self.rect.center[1] - center_moved)
    
        self.prob = prob
        self.update_text("{:03.1f}%".format(100*self.prob))
    
    
    def draw(self, surface):
        surface.fill(pygame.Color("red"), self.rect)
        surface.blit(self.text, self.text_rect)


class ConfirmButton():
    
    width = 80
    height = 80
    
    def __init__(self): 
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/confirm_button.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        
        cx, cy = pygame.display.get_surface().get_rect().center
        self.rect.center = (cx, cy * 9 / 5)
        
        self.click = False
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True
    
    def update_click(self):
        if self.click:
            self.click = False
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class BackButton():
    
    width = 50
    height = 50
    
    def __init__(self): 
        
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/back_button.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = (BackButton.width/2 + 20, BackButton.height/2 + 20)
        
        self.click = False
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True
    
    def update_click(self):
        if self.click == True:
            self.click = False
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class CircuitButton():
    
    width = 50
    height = 50
    
    def __init__(self):
        
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/qiskit.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = (3*CircuitButton.width/2 + 40, CircuitButton.height/2 + 20)
        
        self.click = False
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True
    
    def update_click(self):
        if self.click == True:
            self.click = False
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class TutorialBlock():
    
    width = 200
    height = 50
    
    def __init__(self, pos, message):
        pass

class Knob():
    width = 50
    height = 50

    def __init__(self, pos, angle):

        self.original_image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/knob.jpg'), 
                                            (self.width, self.height))     
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.angle = angle
        
        self.update_text("{:03.1f}π".format(1 * self.angle))  # self.text
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.rect.centerx, self.rect.bottom - self.height - 20)

        self.clickable = True
        self.click = False

    def check_click(self, pos):
        if self.rect.left <= pos[0] and self.rect.right >= pos[0]:
            if self.rect.bottom - self.height <= pos[1] and self.rect.bottom >= pos[1]:
                self.click = True
                pygame.mouse.get_rel()

    def update_rotation(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle*180/pi)
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)  # Put the new rect's center at old center.
    
    def update_text(self, message):
        font = pygame.font.SysFont('timesnewroman', 30)
        self.text = font.render(message, True, pygame.Color("black"))
    
    def update_drag(self):
        if self.click:
            #Dx = abs(pygame.mouse.get_pos()[0] - self.original_image.get_rect().center[0])
            #Dy = abs(pygame.mouse.get_pos()[1] - self.original_image.get_rect().center[1])
            dy = pygame.mouse.get_rel()[1]
            # both dy, dx are negative, so -*- = +
            angle = -dy/30#/Dy if Dy != 0 else 0
    
            self.angle += angle
            
            if self.angle < 0:
                self.angle = 0
            if self.angle > pi:
                self.angle = pi
                
            self.update_rotation()
            self.update_text("{:03.2f}π".format(self.angle/pi))

    def update_with_angle(self, angle):
        
        self.angle = angle
        if self.angle < 0:
            self.angle = 0
        if self.angle > pi:
            self.angle = pi
            
        self.update_rotation()
        self.update_text("{:03.2f}π".format(self.angle/pi))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)
