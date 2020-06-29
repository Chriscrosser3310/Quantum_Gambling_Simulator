import pygame
import qiskit
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import gc
from game_lib.SharedClasses import BackButton, CircuitButton
from game_lib.monty_hall.AliceArrangesBalls import AliceArrangesBalls
from game_lib.monty_hall.BobChoosesDoor import BobChoosesDoor
from game_lib.monty_hall.AliceOpensDoor import AliceOpensDoor
from game_lib.monty_hall.BobSwitchesDoor import BobSwitchesDoor
from game_lib.monty_hall.ShowResult import ShowResult
from game_lib.monty_hall.RunOnRealQC import RunOnRealQC
from game_lib.parameters import BACKGROUND_COLOR, FPS, IMAGE_PATH
from numpy import arctan, sqrt, pi
from copy import deepcopy


class CircuitDisplay():

    wire_height = 200

    def __init__(self, data):
        
        self.data = data
        
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        
        self.pos = (self.screen_rect.center[0], self.screen_rect.center[1])
        
        self.qc = None
        self.qc_list = [qiskit.QuantumCircuit(2, name = 'Alice arranges ball'),
                        qiskit.QuantumCircuit(2, name = 'Bob chooses door'),
                        qiskit.QuantumCircuit(2, name = 'Alice opens door'),
                        qiskit.QuantumCircuit(1, name = 'Bob switches or not'),]
        
        # if circuit is not available
        self.nc_image = pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}/question.png'), (400, 300))
        
        self.update_circuit_0()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.clickable = False

    def update_image(self, qc):
        fig = qc.draw(output='mpl')
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        raw_image = pygame.image.fromstring(raw_data, size, "RGB")
        image_size = [int(size[0]*self.wire_height*qc.width()/size[1]), self.wire_height*qc.width()]
        if image_size[0] > (self.screen.get_size()[0] - 200):
            image_size[0] = (self.screen.get_size()[0] - 200)
            image_size[1] = image_size[0] * size[1]//size[0]
        if image_size[1] > (self.screen.get_size()[1]):
            image_size[1] = (self.screen.get_size()[1])
            image_size[0] = image_size[1] * size[0]//size[1]
        self.image = pygame.transform.scale(raw_image, image_size)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        fig.clear()
        plt.close(fig)
        gc.collect()

    def update_circuit_0(self):
        
        prob_dist = self.data['BallProbDist']
        
        self.qc_list[0].data.clear()
        
        p00, p01, p10 = prob_dist
        if p00 == 1:
            self.qc_list[0].i(0)
        elif p01 == 1:
            self.qc_list[0].x(0)
        elif p10 == 1:
            self.qc_list[0].x(1)
        else:
            angle1 = arctan(sqrt(p01)/sqrt(p00 + p10))*2
            angle2 = arctan(sqrt(p10)/sqrt(p00))*2
            self.qc_list[0].rx(angle1, 0)
            self.qc_list[0].x(0)
            self.qc_list[0].crx(angle2, 0, 1)
            self.qc_list[0].x(0)
        
        qc = qiskit.QuantumCircuit(2)
        qc = qc.compose(self.qc_list[0], [0, 1])
        qc.barrier()
        
        self.update_image(qc)

    def update_circuit_1(self):
        
        choice = self.data['BobChosenDoor']
        
        self.qc_list[1].data.clear()
        
        if choice == -1:
            self.image = self.nc_image
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            return
        elif choice == 0:
            self.qc_list[1].i(0)
        elif choice == 1:
            self.qc_list[1].x(0)
        elif choice == 2:
            self.qc_list[1].x(1)
            
        qc = qiskit.QuantumCircuit(4)
        qc = qc.compose(self.qc_list[0].to_gate(), [0, 1])
        qc = qc.compose(self.qc_list[1], [2, 3])
        qc.barrier()
        
        self.update_image(qc)
        
    def update_circuit_2(self):
        
        choice = self.data['AliceOpenedDoor']
        self.qc_list[2].data.clear()
        
        if choice == -1:
            self.image = self.nc_image
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            return
        elif choice == 0:
            self.qc_list[2].i(0)
        elif choice == 1:
            self.qc_list[2].x(0)
        elif choice == 2:
            self.qc_list[2].x(1)
        
        qc = qiskit.QuantumCircuit(6)
        qc = qc.compose(self.qc_list[0], [0, 1])
        qc = qc.compose(self.qc_list[1].to_gate(), [2, 3])
        qc = qc.compose(self.qc_list[2], [4, 5])
        qc.barrier()
        
        self.update_image(qc)

    def update_circuit_3(self):
        
        prob_dist = self.data['SwitchProbDist']
        self.qc_list[3].data.clear()
        
        p0, p1 = prob_dist
        
        if p0 == 1:
            self.qc_list[3].i(0)
        elif p1 == 1:
            self.qc_list[3].x(0)
        else:
            angle = arctan(sqrt(p1)/sqrt(p0))*2
            self.qc_list[3].ry(angle, 0)
        
        qc = qiskit.QuantumCircuit(7)
        qc = qc.compose(self.qc_list[0].to_gate(), [0, 1])
        qc = qc.compose(self.qc_list[1], [2, 3])
        qc = qc.compose(self.qc_list[2].to_gate(), [4, 5])
        qc = qc.compose(self.qc_list[3], [6])
        qc.barrier()
        
        self.update_image(qc)
    
    def update_circuit_4(self):
        
        qc = qiskit.QuantumCircuit(8, 1)
        
        qc = qc.compose(self.qc_list[0], [0, 1])
        qc = qc.compose(self.qc_list[1], [2, 3])
        qc = qc.compose(self.qc_list[2], [4, 5])
        qc = qc.compose(self.qc_list[3], [6])
        qc.barrier()
        
        qc.x([0,4,5,2])
        qc.mcx([0,1,4,5], 7)
        qc.mcx([4,5,2,3], 7)
        qc.x([1,4,3])
        qc.mcx([0,1,4,5], 7)
        qc.x([0])
        qc.mcx([4,5,2,3], 7)
        qc.x([4,5,2])
        qc.mcx([0,1,4,5], 7)
        qc.mcx([4,5,2,3], 7)
        qc.x([1,4,3])
        qc.cx(6,7)
        qc.barrier()
        qc.measure(7,0)
        
        self.qc = qc
        
        self.update_image(self.qc)
        
    def calculate_result(self):
        if self.qc != None:
            pass
        else:
            raise ValueError('CircuitDisplay.qc not completed')
            
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class MontyHall():

    def __init__(self):

        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.keys = pygame.key.get_pressed()

        self.data = {'BallProbDist': [1/3, 1/3, 1/3],
                     'BobChosenDoor': -1,
                     'AliceOpenedDoor': -1,
                     'SwitchProbDist': [1, 0],
                     'ExpectedValue': 0.0}

        self.stages = [AliceArrangesBalls,
                       BobChoosesDoor,
                       AliceOpensDoor,
                       BobSwitchesDoor,
                       RunOnRealQC,
                       ShowResult,]

        self.stage_index = 0

        self.quit = False
        self.back = False

        cx, cy = self.screen_rect.center
        self.CircuitDisplay = CircuitDisplay(self.data)

        self.BackButton = BackButton()
        self.CircuitButton = CircuitButton()

    def update_circuit(self):
        if self.stage_index == 0:
            self.CircuitDisplay.update_circuit_0()
        elif self.stage_index == 1:
            self.CircuitDisplay.update_circuit_1()
        elif self.stage_index == 2:
            self.CircuitDisplay.update_circuit_2()
        elif self.stage_index == 3:
            self.CircuitDisplay.update_circuit_3()
        elif self.stage_index == 4:
            self.CircuitDisplay.update_circuit_4()
                
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
        current_stage = None
        while not (self.quit or self.back):
            if self.stages[self.stage_index] != type(current_stage):
                current_stage = self.stages[self.stage_index](self.data)
            current_stage.main_loop()
            if current_stage.next_stage == True:
                if self.stage_index == len(self.stages) - 1:
                    self.back = True
                else:
                    self.update_circuit()
                    self.stage_index += 1
            elif current_stage.back == True:
                self.back = True
            elif current_stage.quit == True:
                self.quit = True
            elif current_stage.show_circuit == True:
                self.update_circuit()
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

        
