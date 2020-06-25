import pygame
import qiskit
import os
import sys

import matplotlib
import matplotlib.backends.backend_agg as agg

import numpy


CAPTION = "SHIT"
SCREEN_SIZE = (1000, 500)


class CircuitDisplay():
    
    def __init__(self, pos):
        self.qr = qiskit.QuantumRegister(7)
        self.cr = qiskit.ClassicalRegister(2)
        self.qc = qiskit.QuantumCircuit(self.qr, self.cr)
        self.update_image()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.clickable = False
    
    def update_image(self):
        self.update_circuit()
        fig = self.qc.draw(output = 'mpl')
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        raw_image = pygame.image.fromstring(raw_data, size, "RGB")
        self.image = pygame.transform.scale(raw_image, (SCREEN_SIZE[0], 300))
        
    def update_circuit(self):
        self.qc.x([0,1,2,3,4,5,6])

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)



class Ball():
    
    def __init__(self, pos_list, prob_dist):
        
        self.count = 0
        
        self.pos_list = pos_list
        self.prob_dist = prob_dist
        
        self.width = 50
        self.height = 50   
        self.image = pygame.transform.scale(pygame.image.load('data/prize.png').convert_alpha(), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = self.pos_list[0]
        
        self.clickable = False
        
    def update_distribution(self, prob_dist):
        self.prob_dist = prob_dist
        
    def draw(self, surface):
        self.count += 1
        if self.count == 4:
            index = numpy.random.choice([0, 1, 2], p = self.prob_dist)
            self.rect.center = self.pos_list[index]
            self.count = 0
        surface.blit(self.image, self.rect.topleft)



class Door():
    
    def __init__(self, pos):
        self.width = 100
        self.height = 200    
        self.image = pygame.transform.scale(pygame.image.load('data/door.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.clickable = False
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)



class CheckBox():
    
    def __init__(self, pos):
        self.checked = False
        
        self.width = 30
        self.height = 30 
        self.images = [pygame.transform.scale(pygame.image.load('data/unchecked_checkbox.png'), 
                                              (self.width, self.height)),
                       pygame.transform.scale(pygame.image.load('data/checked_checkbox.png'), 
                                              (self.width, self.height))]
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        
        self.clickable = True
        self.click = False
        
    
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True
    
    def update_click(self):
        if self.click == True:
            self.checked = not self.checked
            self.click = False
            
    def force_unchecked(self):
        self.checked = False
            
    def draw(self, surface):
        if self.checked:
            surface.blit(self.images[1], self.rect.topleft)
        else:
            surface.blit(self.images[0], self.rect.topleft)
        
        
class DoorBar():
    
    def __init__(self, pos, prob):
        self.width = 100
        self.max_height = 200  
        self.rect = pygame.Rect((0,0), (self.width, prob*self.max_height))
        self.rect.bottomleft = (pos[0] - self.width/2, pos[1] + self.max_height/2)
        
        self.prob = prob
        self.update_text("{:04.1f}%".format(100*self.prob)) # self.text
        
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.rect.centerx, self.rect.bottom- self.max_height - 20)
        
        self.clickable = True
        self.click = False
    
    
    def check_click(self, pos):
        if self.rect.left <= pos[0] and self.rect.right >= pos[0]:
            if self.rect.bottom - self.max_height <= pos[1] and self.rect.bottom >= pos[1]:
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
            
            if self.rect.h > self.max_height:
                self.rect.h = self.max_height
            
            elif self.rect.h < 0:
                self.rect.h = 0
            
            center_moved = self.rect.h - original_h 
            self.rect.center = (self.rect.center[0], self.rect.center[1] - center_moved)

            self.prob = self.rect.h/self.max_height
            self.update_text("{:04.1f}%".format(100*self.prob))
    
    
    def update_with_prob(self, prob):
        original_h = self.rect.h
        self.rect.h = 200*prob
        
        center_moved = self.rect.h - original_h
        self.rect.center = (self.rect.center[0], self.rect.center[1] - center_moved)
    
        self.prob = prob
        self.update_text("{:04.1f}%".format(100*self.prob))
    
    
    def draw(self, surface):
        surface.fill(pygame.Color("red"), self.rect)
        surface.blit(self.text, self.text_rect)



class AliceArrangesBalls():
    """
    A class to manage our event, game loop, and overall program flow.
    """
    def __init__(self):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and create our thing.
        """
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pygame.key.get_pressed()
        self.dragged_db = None
        self.checked_cb = None
        
        cx, cy = self.screen_rect.center        
        self.DoorBars = [DoorBar((cx/2, cy), 1/3),
                         DoorBar((cx, cy), 1/3),
                         DoorBar((3*cx/2, cy), 1/3)]
        
        self.Doors = [Door((cx/2, cy)), 
                      Door((cx, cy)),
                      Door((3*cx/2, cy))]
        
        self.CheckBoxes = [CheckBox((cx/2, cy + 120)),
                           CheckBox((cx, cy + 120)),
                           CheckBox((3*cx/2, cy + 120))]
        
        self.Ball = Ball([(cx/2, cy - 50), 
                            (cx, cy - 50), 
                            (3*cx/2, cy - 50)], 
                            [1/3, 1/3, 1/3])
        

    def event_loop(self):
        """
        This is the event loop for the whole program.
        Regardless of the complexity of a program, there should never be a need
        to have more than one event loop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for db in self.DoorBars:
                    db.check_click(event.pos)
                    if db.click == True:
                        self.dragged_db = db
                        break
                for cb in self.CheckBoxes:
                    cb.check_click(event.pos)
                    if cb.click == True:
                        # if True, it means we unchecked it
                        if cb.checked == True:
                            self.checked_cb = None
                        # if not, it means we checked it
                        else:
                            self.checked_cb = cb
                        break
                
                '''
                print(self.DoorBars.index(self.dragged_db) if self.dragged_db != None else None,
                      self.CheckBoxes.index(self.checked_cb) if self.checked_cb != None else None)
                '''
                   
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for db in self.DoorBars:
                    if db.click:
                        db.click = False
                        self.dragged_db = None
                
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.keys = pygame.key.get_pressed() 

    def render(self):
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(pygame.Color("white"))
        
        for db in self.DoorBars:
            db.draw(self.screen)
        
        for d in self.Doors:
            d.draw(self.screen)
            
        for cb in self.CheckBoxes:
            cb.draw(self.screen)
        
        self.Ball.draw(self.screen)
        
        pygame.display.update()

    def main_loop(self):
        """
        This is the game loop for the entire program.
        Like the event_loop, there should not be more than one game_loop.
        """
                
        while not self.done:
            self.event_loop()
            
            # CheckBox
            for cb in self.CheckBoxes:
                if cb != self.checked_cb:
                    cb.force_unchecked()
                cb.update_click()
            
            # DoorBar
            for i in range(3):
                db = self.DoorBars[i]
                cb = self.CheckBoxes[i]
                if not cb.checked:
                    db.update_drag()
            
            prob_sum = sum(self.DoorBars[i].prob for i in range(3))
            if prob_sum != 1:
                if self.checked_cb == None or self.dragged_db == None:
                    for db in self.DoorBars:
                        db.update_with_prob(db.prob/prob_sum)
                else:
                    checked_db = self.DoorBars[self.CheckBoxes.index(self.checked_cb)]
                    checked_prob = checked_db.prob
                    if self.dragged_db.prob > 1 - checked_prob:
                        self.dragged_db.update_with_prob(1 - checked_prob)
                    for db in self.DoorBars:
                        if db != checked_db and db != self.dragged_db:
                            db.update_with_prob(1 - checked_prob - self.dragged_db.prob)
                            
            #Ball
            self.Ball.update_distribution([db.prob for db in self.DoorBars])
            
            self.render()
            self.clock.tick(self.fps)


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_caption(CAPTION)
    #pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_mode(SCREEN_SIZE)
    AliceArrangesBalls().main_loop()
    pygame.quit()
    sys.exit()

main()