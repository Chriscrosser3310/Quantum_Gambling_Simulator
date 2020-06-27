import pygame
import qiskit
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import gc
from game_lib.monty_hall.SharedClasses import BackButton, CircuitButton
from game_lib.monty_hall.AliceArrangesBalls import AliceArrangesBalls
from game_lib.monty_hall.ShowResult import ShowResult
from game_lib.parameters import BACKGROUND_COLOR, FPS
from numpy import arctan, sqrt, pi

class CircuitDisplay():
    
    height = 600
    
    def __init__(self, pos):
        self.qr = qiskit.QuantumRegister(6)
        self.cr = qiskit.ClassicalRegister(1)
        self.qc = qiskit.QuantumCircuit(self.qr, self.cr)
        self.previous_gates = []
        self.update_circuit_0([1/3, 1/3, 1/3])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.clickable = False
        
        
    def update_image(self):
        fig = self.qc.draw(output = 'mpl')
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        raw_image = pygame.image.fromstring(raw_data, size, "RGB")
        self.image = pygame.transform.scale(raw_image, (int(size[0]*self.height/size[1]), self.height))
        fig.clear()
        plt.close(fig)
        gc.collect()
        
    def update_circuit_0(self, prob_dist):
        
        self.qc.data = self.previous_gates
        
        p00, p01, p10 = prob_dist
        
        if p00 == 1:
            self.qc.i(0)
            self.qc.i(0)
            self.qc.i(0)
            self.qc.i(0)
        elif p01 == 1:
            self.qc.x(0)
            self.qc.i(0)
            self.qc.i(0)
            self.qc.i(0)
        elif p10 == 1:
            self.qc.x(1)
            self.qc.i(1)
            self.qc.i(1)
            self.qc.i(1)
        
        else:
            angle1 = arctan(sqrt(p01)/sqrt(p00 + p10))*2
            angle2 = arctan(sqrt(p10)/sqrt(p00))*2
            
            self.qc.ry(angle1, 0)
            self.qc.x(0)
            self.qc.cry(angle2, 0, 1)
            self.qc.x(0)
        
        self.qc.barrier(self.qr)
        self.update_image()
    
    def update_circuit_1(self):
        
        self.qc.data = self.previous_gates

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class MontyHall():
    
    def __init__(self):
        
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS
        
        self.keys = pygame.key.get_pressed()
        
        self.stages = [AliceArrangesBalls(), ShowResult()]
        self.stage_index = 0
        self.quit = False
        self.back = False
        
        cx, cy = self.screen_rect.center
        self.CircuitDisplay = CircuitDisplay((cx, cy))
        
        self.BackButton = BackButton((BackButton.width/2 + 20, BackButton.height/2 + 20))
        self.CircuitButton = CircuitButton((3*CircuitButton.width/2 + 40, CircuitButton.height/2 + 20))
    
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
                    self.BackButton.check_click(event.pos)
                    self.CircuitButton.check_click(event.pos)
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.keys = pygame.key.get_pressed()
        
    def render(self):
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))
       
        self.CircuitDisplay.draw(self.screen)
        
        self.BackButton.draw(self.screen)
        self.CircuitButton.draw(self.screen)
        
        pygame.display.update()
        
    def main_loop(self):
    
        while not (self.quit or self.back):
            current_stage = self.stages[self.stage_index]
            current_stage.main_loop()
            if current_stage.next_stage == True:
                self.stage_index += 1
                self.CircuitDisplay.previous_gates = self.CircuitDisplay.qc.data
                if self.stage_index == len(self.stages):
                    self.back = True
            elif current_stage.back == True:
                self.back = True
            elif current_stage.quit == True:
                self.quit = True
            elif current_stage.show_circuit == True:
                if self.stage_index == 0:
                    self.CircuitDisplay.update_circuit_0([db.prob for db in current_stage.DoorBars])
                elif self.stage_index == 1:
                    self.CircuitDisplay.update_circuit_1()
                while (current_stage.show_circuit and not (self.quit or self.back)):
                    self.event_loop()
                    if self.BackButton.click:
                        self.BackButton.update_click()
                        self.back = True
                    elif self.CircuitButton.click:
                        self.CircuitButton.update_click()
                        current_stage.show_circuit = False
                    self.render()
                    self.clock.tick(self.fps)
            else:
                raise ValueError('Stage quits without proceeding')
    
