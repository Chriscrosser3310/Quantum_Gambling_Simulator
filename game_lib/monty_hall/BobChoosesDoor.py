import pygame
import numpy
from game_lib.SharedClasses import ConfirmButton, BackButton, CircuitButton, TutorialBlock
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH


class DoorBob():
    
    width = 100
    height = 200

    def __init__(self, pos, data):
        
        self.data = data
        
        self.bob_image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/bob.jpg'),
                                              (self.width*3//2, self.height*3//4))
        
        self.bob_rect = self.bob_image.get_rect()
        self.bob_rect.center = (pos[0] - self.width*4//3, pos[1])
        
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/door.png'),
                                            (self.width, self.height))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] - self.width/2, pos[1] - self.height/2)

        self.click = False
        
    def update_click(self):
        if self.click:
            self.checked = not self.checked
            self.click = False
            self.data['BobChosenDoor'] = -1
            
    def force_unchecked(self):
        self.checked = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True
    
    def draw(self, surface):
        if self.checked:
            surface.blit(self.bob_image, self.bob_rect.topleft)
            surface.blit(self.image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)



class BobChoosesDoor:
    def __init__(self, data):
        self.data = data
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        self.checked_db = None

        cx, cy = self.screen_rect.center

        self.DoorBobs = [DoorBob((cx / 2, cy), self.data),
                           DoorBob((cx, cy), self.data),
                           DoorBob((3 * cx / 2, cy), self.data)]

        self.ConfirmButton = ConfirmButton()
        self.CircuitButton = CircuitButton()
        self.BackButton = BackButton()

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

                    for db in self.DoorBobs:
                        db.check_click(event.pos)
                        if db.click:
                            # if True, it means we unchecked it
                            if db.checked:
                                self.checked_db = None
                            # if not, it means we checked it
                            else:
                                self.checked_db = db
                            break

                    self.ConfirmButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)

    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))
        for db in self.DoorBobs:
            db.draw(self.screen)
        self.ConfirmButton.draw(self.screen)
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)

        pygame.display.update()


    def main_loop(self):
        while not (self.quit or self.next_stage or self.back or self.show_circuit):
            self.event_loop()

            # CheckBob
            for i in range(0, 3):
                db = self.DoorBobs[i]
                if db != self.checked_db:
                    db.force_unchecked()
                else:
                    self.data["BobChosenDoor"] = i
                db.update_click()

            if self.ConfirmButton.click:
                self.ConfirmButton.update_click()
                # continue only when bob's choice has been set
                if self.data["BobChosenDoor"] != -1:
                    self.next_stage = True
                    
            elif self.BackButton.click:
                self.BackButton.update_click()
                self.back = True
            elif self.CircuitButton.click:
                self.CircuitButton.update_click()
                self.show_circuit = True

            self.render()
            self.clock.tick(self.fps)
