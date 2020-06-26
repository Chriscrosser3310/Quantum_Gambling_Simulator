import pygame

class ConfirmButton():
    
    width = 80
    height = 80
    
    def __init__(self, pos): 
        self.image = pygame.transform.scale(pygame.image.load('data/confirm_button.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.clickable = True
        self.click = False
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True
    
    def update_click(self):
        if self.click == True:
            self.click = False
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class BackButton():
    
    width = 50
    height = 50
    
    def __init__(self, pos): 
        self.image = pygame.transform.scale(pygame.image.load('data/back_button.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.clickable = True
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
    
    def __init__(self, pos): 
        self.image = pygame.transform.scale(pygame.image.load('data/qiskit.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.clickable = True
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

