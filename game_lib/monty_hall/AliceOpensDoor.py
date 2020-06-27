import pygame
import numpy
from game_lib.monty_hall.SharedClasses import DoorBar, ConfirmButton, BackButton, CircuitButton, TutorialBlock
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH



class DoorAlice():
    
    width = 100
    height = 200

    def __init__(self, pos, data):
        
        self.data = data
        
        self.bob_image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/bob.jpg'),
                                              (self.width*3//2, self.height*3//4))
        
        self.bob_rect = self.bob_image.get_rect()
        self.bob_rect.center = (pos[0] - self.width*4//3, pos[1])
        
        self.chosen = False
        
        self.alice_image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/alice.jpg'),
                                              (self.width*3//2, self.height*3//4))
        
        self.alice_rect = self.alice_image.get_rect()
        self.alice_rect.center = (pos[0], pos[1] - self.height*9//8)
        
        self.images = [pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/door.png'),
                                            (self.width, self.height)),
                      pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/opened_door.png'),
                                            (self.width, self.height*2000//1459))]
        
        self.rect = self.images[0].get_rect()
        self.rect.topleft = (pos[0] - self.width/2, pos[1] - self.height/2)

        self.click = False
        
    def update_click(self):
        if self.click:
            self.checked = not self.checked
            self.click = False
            self.data['AliceOpenedDoor'] = -1
            
    def force_unchecked(self):
        self.checked = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and not self.chosen:
            self.click = True
    
    def draw(self, surface):
        if self.chosen:
            surface.blit(self.bob_image, self.bob_rect.topleft)
            surface.blit(self.images[0], self.rect.topleft)
        else:    
            if self.checked:
                surface.blit(self.alice_image, self.alice_rect.topleft)
                surface.blit(self.images[1], self.rect.topleft)
            else:
                surface.blit(self.images[0], self.rect.topleft)



class AliceOpensDoor:
    def __init__(self, data):
        self.data = data
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        self.checked_da = None

        cx, cy = self.screen_rect.center
        
        self.DoorBars = [DoorBar((cx/2, cy), self.data['BallProbDist'][0]),
                         DoorBar((cx, cy), self.data['BallProbDist'][1]),
                         DoorBar((3*cx/2, cy), self.data['BallProbDist'][2])]

        self.DoorAlices = [DoorAlice((cx / 2, cy), self.data),
                           DoorAlice((cx, cy), self.data),
                           DoorAlice((3 * cx / 2, cy), self.data)]

        self.ConfirmButton = ConfirmButton((cx, cy * 9 / 5))
        self.CircuitButton = CircuitButton((3 * CircuitButton.width / 2 + 40, CircuitButton.height / 2 + 20))

        self.BackButton = BackButton(
            (BackButton.width / 2 + 20, BackButton.height / 2 + 20))

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

                    for da in self.DoorAlices:
                        da.check_click(event.pos)
                        if da.click:
                            # if True, it means we unchecked it
                            if da.checked:
                                self.checked_da = None
                            # if not, it means we checked it
                            else:
                                self.checked_da = da
                            break


                    self.ConfirmButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)

    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))
        for db in self.DoorBars:
            db.draw(self.screen)
        for da in self.DoorAlices:
            da.draw(self.screen)
        self.ConfirmButton.draw(self.screen)
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)

        pygame.display.update()


    def main_loop(self):
        
        self.DoorAlices[self.data['BobChosenDoor']].chosen = True
        
        while not (self.quit or self.next_stage or self.back or self.show_circuit):
            self.event_loop()           

            # CheckAlice
            for i in range(0, 3):
                da = self.DoorAlices[i]
                if da != self.checked_da:
                    da.force_unchecked()
                else:
                    self.data["AliceOpenedDoor"] = i
                    open_index = i
                    add_index = (i + 1) % 3
                    prob_dist = list(self.data["BallProbDist"])
                    prob_dist[add_index] += prob_dist[open_index]
                    prob_dist[open_index] = 0
                    for j in range(0, 3):
                        self.DoorBars[j].update_with_prob(prob_dist[j])
                
                da.update_click()
            
            if self.data["AliceOpenedDoor"] == -1:
                for j in range(0, 3):
                    self.DoorBars[j].update_with_prob(self.data["BallProbDist"][j])

            if self.ConfirmButton.click:
                self.ConfirmButton.update_click()
                # continue only when bob's choice has been set
                if self.data["AliceOpenedDoor"] != -1:
                    self.next_stage = True
                    self.data["BallProbDist"][add_index] += self.data["BallProbDist"][open_index]
                    self.data["BallProbDist"][open_index] = 0
                    
            elif self.BackButton.click:
                self.BackButton.update_click()
                self.back = True
            elif self.CircuitButton.click:
                self.CircuitButton.update_click()
                self.show_circuit = True

            self.render()
            self.clock.tick(self.fps)
