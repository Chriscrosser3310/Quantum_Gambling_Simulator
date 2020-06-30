import pygame
import numpy
from game_lib.SharedClasses import Door, DoorBar, ConfirmButton, BackButton, CircuitButton, TutorialBlock
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH


#flick Bob's image while setting his decision Prob
class BobImage():
    width = 150
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
            index = numpy.random.choice([0, 1], p = self.prob_dist)
            self.rect.center = self.pos_list[index]
            self.count = 0
        surface.blit(self.image, self.rect.topleft)

    
#change the image of Door while Alice chose to open it
class OpenedDoor():
    
    width = 100
    height = 200

    def __init__(self, pos):
        
        self.alice_image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/alice.jpg'),
                                              (self.width*3//2, self.height*3//4))
        
        self.alice_rect = self.alice_image.get_rect()
        self.alice_rect.center = (pos[0] - self.width*4//3, pos[1])
        
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/opened_door.png'),
                                            (self.width, self.height*2000//1459))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] - self.width/2, pos[1] - self.height/2)

        self.click = False
    
    def draw(self, surface):
        surface.blit(self.alice_image, self.alice_rect.topleft)
        surface.blit(self.image, self.rect.topleft)
                                                        


class DoorBarBob(DoorBar):
    
    def __init__(self, pos, prob):
        DoorBar.__init__(self, pos, prob)
    
    def draw(self, surface):
        surface.fill(pygame.Color("yellow"), self.rect)
        surface.blit(self.text, self.text_rect)



class BobSwitchesDoor():
    
    #expect receiving an int(0,1,2) represents which Door Alice opens
    def __init__(self, data):

        self.data = data
        self.Alice = self.data['AliceOpenedDoor']
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS
        
        self.keys = pygame.key.get_pressed()

        self.dragged_db = None
        self.checked_cb = None
        

        cx, cy = self.screen_rect.center
        
        self.DoorPos = [(cx/2, cy),(cx, cy),(1.5*cx, cy)]
        
        self.BobPos = [(cx/2 - Door.width*4//3, cy),
                       (cx - Door.width*4//3, cy),
                       (3*cx/2 - Door.width*4//3, cy)]
        
         # swap if bob did not choose door 00, to ensure |0> is bob's initial choice
        if self.data['BobChosenDoor'] != 0:
            choice = self.data['BobChosenDoor']
            self.DoorPos[choice], self.DoorPos[0] = self.DoorPos[0], self.DoorPos[choice]
            self.BobPos[choice], self.BobPos[0] = self.BobPos[0], self.BobPos[choice]
        
        # swap Alice as well if Alice choosed 0
        if self.Alice == 0:
            self.Alice = choice
        
        #remove Alice's choice from Bob's image
        self.BobPos.pop(self.Alice)
        
        #remove and take out the pos of Alice's Choice
        self.OpenedDoorPos = self.DoorPos.pop(self.Alice)
        
        self.DoorBars = [DoorBarBob(self.DoorPos[0], self.data['SwitchProbDist'][0]),
                         DoorBarBob(self.DoorPos[1], self.data['SwitchProbDist'][1])]
        
        self.Doors = [Door(self.DoorPos[0]),
                      Door(self.DoorPos[1])]
        
        self.BobImage = BobImage(self.BobPos, self.data['SwitchProbDist'])

        self.OpenedDoor = OpenedDoor(self.OpenedDoorPos)


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
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))

        for db in self.DoorBars:
            db.draw(self.screen)

        for d in self.Doors:
            d.draw(self.screen)

        #Capital OpenedDoor is the object pointing to class OpenedDoor(pos)
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
            
            self.data['SwitchProbDist'] = [db.prob for db in self.DoorBars]
            self.BobImage.update_distribution([db.prob for db in self.DoorBars])

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
            
                
                        

        


        
        
        
