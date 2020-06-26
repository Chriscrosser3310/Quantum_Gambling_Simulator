import pygame
pygame.init()

win=pygame.display.set_mode((1000,800))
white=(255,255,255)
black=(0,0,0)
gray=(100,100,100)


class button():
    def __init__(self, color, x,y,width,height,text=''):
        self.color=color
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text

    #method to draw the button on the screen
    def drawButton(self,win,outline=None):
        if outline:
            #once if there is an outline
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text !='':
            font=pygame.font.SysFont('comicsans',60)
            text=font.render(self.text, 1, (0,0,0))
            #change the position and the size of text symoutaneously with the button
            win.blit(text, (self.x+(self.width/2-text.get_width()/2), self.y+ (self.height/2-text.get_height()/2)))


    def touchButton(self,mouse):
        if mouse[0]>self.x and mouse[0]<self.x+self.width:
            if mouse[1]>self.y and mouse[1]<self.y+self.height:
                return True

        return False

def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill(white)
    for alpha in range(0,255):
        fade.set_alpha(alpha)
        grayButton.drawButton(win)
        win.blit(fade,(0,0))
        pygame.display.update()
        pygame.time.delay(3)

def homePage():
    win.fill(white)
    grayButton.drawButton(win)




run=True
grayButton = button(gray,375,400,250,50,'Monty Hall')
backButton = button(gray,2,2,200,100,'Back <--')
back=0

while run:
    homePage()
    pygame.display.update()


    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()

        
        #hit the Monty Hall button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if grayButton.touchButton(mouse):
                print('clicked')
                fade(1000,800)
               
                        


        if event.type == pygame.MOUSEMOTION:
            if grayButton.touchButton(mouse):
                grayButton.color=black
            else:
                grayButton.color=gray

        
        if event.type == pygame.QUIT:
            run=False
            pygame.quit()
            quit()



    
