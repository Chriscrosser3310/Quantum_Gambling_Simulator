import pygame
import numpy
from game_lib.monty_hall.SharedClasses import Door, DoorBar, ConfirmButton, BackButton, CircuitButton, TutorialBlock
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH


class Ball():
    
    width = 30
    height = 30  
    
    def __init__(self, pos_list, prob_dist):
        
        self.count = 0
        
        self.pos_list = pos_list
        self.prob_dist = prob_dist
         
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/ball.png'), 
                                            (self.width, self.height))     
        self.rect = self.image.get_rect()
        self.rect.center = self.pos_list[0]
        
        
    def update_distribution(self, prob_dist):
        self.prob_dist = prob_dist
        
    def draw(self, surface):
        self.count += 1
        if self.count == 4:
            index = numpy.random.choice([0, 1, 2], p = self.prob_dist)
            self.rect.center = self.pos_list[index]
            self.count = 0
        surface.blit(self.image, self.rect.topleft)


class CheckBox():
    
    width = 30
    height = 30 
    
    def __init__(self, pos):
        self.checked = False
        
        
        self.images = [pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/unchecked_checkbox.png'), 
                                              (self.width, self.height)),
                       pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/checked_checkbox.png'), 
                                              (self.width, self.height))]
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        
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
        
        


class AliceArrangesBalls():
    """
    A class to manage our event, game loop, and overall program flow.
    """
    def __init__(self, data):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and create our thing.
        """
        self.data = data
        
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()
        
        self.dragged_db = None
        self.checked_cb = None
        
        cx, cy = self.screen_rect.center
        self.DoorBars = [DoorBar((cx/2, cy), self.data['BallProbDist'][0]),
                         DoorBar((cx, cy), self.data['BallProbDist'][1]),
                         DoorBar((3*cx/2, cy), self.data['BallProbDist'][2])]
        
        self.Doors = [Door((cx/2, cy)), 
                      Door((cx, cy)),
                      Door((3*cx/2, cy))]
        
        self.CheckBoxes = [CheckBox((cx/2, cy + Door.height/2 + 20)),
                           CheckBox((cx, cy + Door.height/2 + 20)),
                           CheckBox((3*cx/2, cy + Door.height/2 + 20))]
        
        self.Ball = Ball([(cx/2, cy - Door.height/4), 
                            (cx, cy - Door.height/4), 
                            (3*cx/2, cy - Door.height/4)], 
                            self.data['BallProbDist'])
        
        self.ConfirmButton = ConfirmButton()
        self.BackButton = BackButton()
        self.CircuitButton = CircuitButton()
        
        self.tutorial_on = False
        #self.TutorialBlocks = [TutorialBlock()]
        
        self.next_stage = False
        self.quit = False
        self.back = False
        self.show_circuit = False
        

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
                    
                    self.ConfirmButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)
                
                '''
                print(self.DoorBars.index(self.dragged_db) if self.dragged_db != None else None,
                      self.CheckBoxes.index(self.checked_cb) if self.checked_cb != None else None)
                '''
                   
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for db in self.DoorBars:
                        if db.click:
                            db.click = False
                            self.dragged_db = None
                            break
                
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.keys = pygame.key.get_pressed()
                

    def render(self):
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))
        
        for db in self.DoorBars:
            db.draw(self.screen)
        
        for d in self.Doors:
            d.draw(self.screen)
            
        for cb in self.CheckBoxes:
            cb.draw(self.screen)
        
        self.Ball.draw(self.screen)
        self.ConfirmButton.draw(self.screen)
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)
        
        pygame.display.update()
        

    def main_loop(self):
        """
        This is the game loop for the entire program.
        Like the event_loop, there should not be more than one game_loop.
        """
                
        while not (self.quit or self.next_stage or self.back or self.show_circuit):
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
                            
            self.data['BallProbDist'] = [db.prob for db in self.DoorBars]
                                        
            #Ball
            self.Ball.update_distribution([db.prob for db in self.DoorBars])
            
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

