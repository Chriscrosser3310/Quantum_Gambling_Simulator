import pygame
import numpy
from game_lib.monty_hall.SharedClasses import ConfirmButton, BackButton, CircuitButton, TutorialBlock
from game_lib.parameters import BACKGROUND_COLOR, FPS


class Caption:
    width = 800
    height = 100

    def __init__(self, pos):
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Door:
    width = 100
    height = 200

    def __init__(self, pos, bob):
        self.bob = bob
        self.image = pygame.transform.scale(pygame.image.load('assets/images/door.png'),
                                            (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.clickable = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.bob.click = True


class CheckBob:
    width = 150
    height = 150

    def __init__(self, pos, data):
        self.data = data
        self.checked = False

        self.images = [pygame.transform.scale(pygame.image.load('assets/images/bob.jpg'),
                                              (self.width, self.height)),
                       pygame.transform.scale(pygame.image.load('assets/images/bob.jpg'),
                                              (0, 0))]
        self.rect = self.images[0].get_rect()
        self.rect.center = pos

        self.clickable = True
        self.click = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True

    def update_click(self):
        if self.click:
            self.checked = not self.checked
            self.click = False
            self.data["BobChosenDoor"] = -1

    def force_unchecked(self):
        self.checked = False

    def draw(self, surface):
        if self.checked:
            surface.blit(self.images[0], self.rect.topleft)
        else:
            surface.blit(self.images[1], self.rect.topleft)


class BobChoosesDoor:
    def __init__(self, data):
        self.data = data
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        self.dragged_db = None
        self.checked_cb = None

        cx, cy = self.screen_rect.center

        self.Doors = [Door((cx / 2, cy), None),
                      Door((cx, cy), None),
                      Door((3 * cx / 2, cy), None)]

        self.CheckBobs = [CheckBob((cx / 2, cy - Door.height / 2 - 80), data),
                          CheckBob((cx, cy - Door.height / 2 - 80), data),
                          CheckBob((3 * cx / 2, cy - Door.height / 2 - 80), data)]

        for i in range(0, 3):
            self.Doors[i].bob = self.CheckBobs[i]

        self.ConfirmButton = ConfirmButton((cx, cy * 8 / 5))
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

                    for door in self.Doors:
                        door.check_click(event.pos)

                    for cb in self.CheckBobs:
                        cb.check_click(event.pos)
                        if cb.click:
                            # if True, it means we unchecked it
                            if cb.checked:
                                self.checked_cb = None
                            # if not, it means we checked it
                            else:
                                self.checked_cb = cb
                            break

                    self.ConfirmButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)

    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))
        for d in self.Doors:
            d.draw(self.screen)
        for cb in self.CheckBobs:
            cb.draw(self.screen)
        self.ConfirmButton.draw(self.screen)
        self.BackButton.draw(self.screen)

        pygame.display.update()

    def main_loop(self):
        while not (self.quit or self.next_stage or self.back or self.show_circuit):
            self.event_loop()

            # CheckBob
            for i in range(0, 3):
                cb = self.CheckBobs[i]
                if cb != self.checked_cb:
                    cb.force_unchecked()
                else:
                    self.data["BobChosenDoor"] = i
                cb.update_click()

            if self.ConfirmButton.click:
                self.ConfirmButton.update_click()
                # continue only when bob's choice has been set
                if self.data["BobChosenDoor"] != -1:
                    self.next_stage = True
            elif self.BackButton.click:
                self.BackButton.update_click()
                self.back = True

            self.render()
            self.clock.tick(self.fps)
