import pygame
import numpy
from game_lib.monty_hall.SharedClasses import ConfirmButton, BackButton, CircuitButton, TutorialBlock
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH

white=(255,255,255)
balck=(0,0,0)
yellow=(0,255,0)


#flick Bob's image while setting his decision Prob
class BobImage():
    width = 100
    height = 150

    def __init__(self, pos_list, prob_dist):

        self.count = 0

        self.pos_list = pos_list
        self.prob_dist = prob_dist

        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/bob.jpg'),
                                            (self.width,self.height))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos_list[0]

        self.clickable = False

    def update_distribution(self,prob_dist):
        self.prob_dist = prob_dist

    def draw(self, surface):
        self.count +=1
        if self.count == 4:
            index = numpy.random.choice([0,1], p = self.prob_dist)
            self.rect.center = self.pos_list[index]
            self.count = 0
        surface.blit(self.image, self.rect.topleft)

    
#change the image of Door while Alice chose to open it
class openedDoor():
    width = 100
    height = 200

    def __init__(self, pos):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/opened_door.png'),
                                            (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.clickable = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.toplet)
                                                        
    

class Door():
    width = 100
    height = 200

    def __init__(self, pos):
        
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/door.png'),
                                            (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.clickable = False


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class DoorBar():

    width = Door.width
    height = Door.height
    

    def __init__(self, pos, prob):
  
        self.rect = pygame.Rect((0,0),(self.width, prob*self.height))
        self.rect.bottomleft = (pos[0] - self.width/2, pos[1] + self.height/2)

        self.prob = prob
        #call the update_text function defined in the following
        self.update_text("{:03.1f}%".format(100*self.prob))

        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.rect.centerx, self.rect.bottom - self.height -20)

        self.clickable = True
        self.click = False

    #check if mouse is over the Door's section
    def check_click(self, pos):
        if self.rect.left <= pos[0] and self.rect.right >= pos[0]:
            if self.rect.bottom - self.height <= pos[1] and self.rect.bottom >= pos[1]:
                self.click = True
                pygame.mouse.get_rel()


    def update_text(self, message):
        font = pygame.font.SysFont('timesnewroman', 30)
        self.text = font.render(message, True, black)


    def update_drag(self):
        if self.click:
            #take the dragged height
            dh = pygame.mouse.get_rel()[1]
            original_h =  self.rect.h
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
        surface.fill(yellow, self.rect)
        surface.blit(self.text, self.text_rect)

class BobSwitchesDoor():
    
    #expect receiving an int(0,1,2) represents which Door Alice opens
    def __init__(self, AliceChoice):

        self.data = data
        self.Alice = AliceChoice
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS


        self.dragged_db = None
        self.checked_cb = None
        

        cx, cy = self.screen_rect.center
        self.DoorPos = [(cx/2, cy),(cx, cy),(1.5*cx, cy)]
        
        self.BobPos = [(cx/2, cy - Door.height/2),
                       (cx, cy - Door.height/2),
                       (3*cx/2, cy - Door.height/2)]
        #remove Alice's choice from Bob's image
        self.BobPos.remove(self.Alice)
        
        #remove and take out the pos of Alice's Choice
        self.openedDoorPos = self.DoorPos.pop(self.Alice)
        
        #Set the qubit default value of Bob's choice is 50:50
        #here I assume BobPorbDist should be len2
        self.DoorBars = [DoorBar(self.DoorPos[0], self.data['BobProbDist'][0]),
                         DoorBar(self.DoorPos[1], self.data['BobProbDist'][1])]
        
        self.Doors = [Door(self.DoorPos[0]),
                      Door(self.DoorPos[1])]

        self.Bob = BobImage(self.BobPos, [0.5,0.5])

        self.OpenedDoor = openedDoor(self.openedDoorPos)


        self.ConfirmButton = ConfirmButton((cx, cy* 8/5))
        self.BackButton = BackButton((BackButton.width/2 + 20, BackButton.height/2 + 20))
        self.CircuitButton = CircuitButton((3*CircuitButton.width/2 + 40, CircuitButton.height/2 + 20))

        self.tutorial_on = False
        #self.TutorialBlocks = [TutorialBlock()]
        
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

                    for db in self.DoorBars:
                        db.check_click(event.pos)
                        if db.click == True:
                            self.dragged_db = db
                            break

                    self.ConfirmButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for db in self.DoorBars:
                        if db.click:
                            db.click = False
                            self.dragged_db = None
                            break


    def render(self):


        self.screen.fill(white)

        for db in self.DoorBars:
            db.draw(self.screen)

        for d in self.Doors:
            d.draw(self.screen)

        #Capital OpenedDoor is the object pointing to class openedDoor(pos)
        self.OpenedDoor.draw(self.screen)
        
        self.BobImage.draw(self.screen)
        self.ConfirmButton.draw(self.screen)
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)
        
        pygame.display.update()


    def main_loop(self):

        while not (self.quit or self.next_stage or self.back or self.show_circuit):
            self.event_loop()

            #DoorBar
            for db in self.DoorBars:
                db.update_drag()

            
            prob_sum = sum(self.DoorBars[i].prob for i in range(2))

            #if prob_sum !=1:
                
            if self.dragged_db == None:
                for db in self.DoorBars:
                    db.update_with_prob(db.prob/prob_sum)

            else:
                for db in self.DoorBars:
                    if db != self.dragged_db:
                        db.update_with_prob(1-self.dragged_db.prob)
                        

            if self.ConfirmButton.click:
                self.ConfirmButton.update_click()
                self.data['BobProbDist'] = [db.prob for db in self.DoorBars]
                self.next_stage = True 
            elif self.BackButton.click:
                self.BackButton.update_click()
                self.back = True
            elif self.CircuitButton.click:
                self.CircuitButton.update_click()
                self.show_circuit = True


            self.render()
            self.clock.tick(self.fps)


        return self.dragged_db.prob
            
                
                        

        


        
        
        
