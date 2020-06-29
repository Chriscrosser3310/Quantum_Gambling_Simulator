import pygame
from game_lib.SharedClasses import DoorBar, ConfirmButton, BackButton, CircuitButton, TutorialBlock, Knob
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH



class Caption:
    width = 800
    height = 200

    def __init__(self, pos):
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        font = pygame.font.SysFont('timesnewroman', 30)
        self.text = font.render('Let\'s discuss a strategy...', True, pygame.Color("black"))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos

    def draw(self, surface):
        surface.blit(self.text, self.text_rect)


class Bob:
    width = 200
    height = 200

    def __init__(self, pos):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/bob.jpg'),
                                            (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class Alice:
    width = 200
    height = 200

    def __init__(self, pos):
        self.image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/alice.jpg'),
                                            (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class StartStage:
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

        self.dragged_k = None
        self.checked_cb = None

        cx, cy = self.screen_rect.center
        self.alice = Alice((cx - 100, 1.2 * cy))
        self.bob = Bob((cx + 100, 1.2 * cy))
        self.Knobs = [Knob((cx / 2, 0.5 * cy), 0)]

        self.caption = Caption((cx, 0.5 * cy))

        # self.Doors = [Door((cx / 2, cy)),
        #               Door((cx, cy)),
        #               Door((3 * cx / 2, cy))]
        #
        # self.CheckBoxes = [CheckBox((cx / 2, cy + Door.height / 2 + 20)),
        #                    CheckBox((cx, cy + Door.height / 2 + 20)),
        #                    CheckBox((3 * cx / 2, cy + Door.height / 2 + 20))]
        #
        # self.Ball = Ball([(cx / 2, cy - Door.height / 4),
        #                   (cx, cy - Door.height / 4),
        #                   (3 * cx / 2, cy - Door.height / 4)],
        #                  self.data['BallProbDist'])

        self.ConfirmButton = ConfirmButton()
        self.BackButton = BackButton()
        self.CircuitButton = CircuitButton()

        self.tutorial_on = False
        # self.TutorialBlocks = [TutorialBlock()]

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

                    for k in self.Knobs:
                        k.check_click(event.pos)
                        if k.click == True:
                            self.dragged_k = k
                            break

                    # for cb in self.CheckBoxes:
                    #     cb.check_click(event.pos)
                    #     if cb.click == True:
                    #         # if True, it means we unchecked it
                    #         if cb.checked == True:
                    #             self.checked_cb = None
                    #         # if not, it means we checked it
                    #         else:
                    #             self.checked_cb = cb
                    #         break

                    self.ConfirmButton.check_click(event.pos)
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)

                '''
                print(self.Knobs.index(self.dragged_k) if self.dragged_k != None else None,
                      self.CheckBoxes.index(self.checked_cb) if self.checked_cb != None else None)
                '''

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
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))

        for k in self.Knobs:
            k.draw(self.screen)

        # for d in self.Doors:
        #     d.draw(self.screen)
        #
        # for cb in self.CheckBoxes:
        #     cb.draw(self.screen)

        # self.Ball.draw(self.screen)

        self.bob.draw(self.screen)
        self.alice.draw(self.screen)
        self.ConfirmButton.draw(self.screen)
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)
        self.caption.draw(self.screen)

        pygame.display.update()

    def main_loop(self):
        """
        This is the game loop for the entire program.
        Like the event_loop, there should not be more than one game_loop.
        """

        while not (self.quit or self.next_stage or self.back or self.show_circuit):
            self.event_loop()

            # CheckBox
            # for cb in self.CheckBoxes:
            #     if cb != self.checked_cb:
            #         cb.force_unchecked()
            #     cb.update_click()

            # Knob
            for i in range(1):
                k = self.Knobs[i]
                # cb = self.CheckBoxes[i]
                # if not cb.checked:
                k.update_drag()

            # prob_sum = sum(self.Knobs[i].prob for i in range(3))
            # if prob_sum != 1:
            #     if self.checked_cb == None or self.dragged_k == None:
            #         for k in self.Knobs:
            #             k.update_with_prob(k.prob / prob_sum)
            #     else:
            #         checked_k = self.Knobs[self.CheckBoxes.index(self.checked_cb)]
            #         checked_prob = checked_k.prob
            #         if self.dragged_k.prob > 1 - checked_prob:
            #             self.dragged_k.update_with_prob(1 - checked_prob)
            #         for k in self.Knobs:
            #             if k != checked_k and k != self.dragged_k:
            #                 k.update_with_prob(1 - checked_prob - self.dragged_k.prob)
            #
            # self.data['BallProbDist'] = [k.prob for k in self.Knobs]

            # Ball
            # self.Ball.update_distribution([k.prob for k in self.Knobs])

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
