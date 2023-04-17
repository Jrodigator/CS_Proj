import pygame
# import sprite manager
from utils import load_sprite
import game
from sys import exit

class Title_Screen:
    
    def __init__(self):
        self.__init__pygame()
        self.screen = pygame.display.set_mode((696, 528))
        self.title_font = pygame.font.Font("Assets/minecraftfont.otf",50)
        self.game_name = self.title_font.render('Hive Invaders',False,(85,69,15))
        self.game_message = self.title_font.render('Press \'Space\'to Start',False,(85,69,15))
        self.game_name_rect=self.game_name.get_rect(center=(348,132))
        self.game_message_rect=self.game_message.get_rect(center=(348,396))
        self.bee=pygame.image.load("Assets/Bee.png")
        self.bee=pygame.transform.rotozoom(self.bee,0,1.5)
        self.beerect=self.bee.get_rect(center=(348,264))   

    def __init__pygame(self):
        pygame.init()
        pygame.display.set_caption("Protect The Hive")
    
    def draw(self):
            self.screen.fill((254, 200, 9))
            self.screen.blit(self.game_name,self.game_name_rect)
            self.screen.blit(self.game_message,self.game_message_rect)
            self.screen.blit(self.bee,self.beerect)
            pygame.display.flip()
            #self.clock.tick(60)

    def title_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                    instance=Menu()
                    instance.menu_loop()
            self.draw()
class Menu:
    
    def __init__(self):
        self.__init__pygame()
        self.screen = pygame.display.set_mode((696, 528))
        self.bg = pygame.transform.scale(load_sprite("menubackground"), (696, 528))
        self.playimage=pygame.image.load("Assets/playbtn.png")
        self.levelsimage=pygame.image.load("Assets/levelsbtn.png")
        self.scoresimage=pygame.image.load("Assets/scoresbtn.png")
        self.quitimage=pygame.image.load("Assets/quitbtn.png")
        self.playrect=self.playimage.get_rect(topleft= (80,30))
        self.levelsrect=self.levelsimage.get_rect(topleft= (80,110))
        self.scoresrect=self.scoresimage.get_rect(topleft= (80,190))
        self.quitrect=self.quitimage.get_rect(topleft= (80,270))
        
        # Game Clock & Speed
        self.clock = pygame.time.Clock()
        self.fps = 60

        

    def __init__pygame(self):
        pygame.init()
        pygame.display.set_caption("Protect The Hive")
    
    def draw(self):
        self.screen.fill((0, 0, 255))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.playimage,self.playrect)
        self.screen.blit(self.levelsimage,self.levelsrect)
        self.screen.blit(self.scoresimage,self.scoresrect)
        self.screen.blit(self.quitimage,self.quitrect)    
        pygame.display.flip()
        self.clock.tick(60)

    def menu_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.MOUSEBUTTONUP:
                    mouse_pos=pygame.mouse.get_pos()
                    if self.playrect.collidepoint(mouse_pos):
                        instance= game.Game()
                        instance.game_loop()
                    elif  self.scoresrect.collidepoint(mouse_pos):
                        print("score")#score() or level select()
                        instance = Scores()
                        instance.score_loop()
                    elif  self.quitrect.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()
                    elif  self.levelsrect.collidepoint(mouse_pos):
                        instance = Levels()
                        instance.level_loop()
            self.draw()

class Levels:
        def __init__(self):

            self.screen = pygame.display.set_mode((696, 528))
            self.bg = pygame.transform.scale(load_sprite("levelsbg"), (696, 528))
            self.level1=pygame.Rect(90,25,150,50)
            self.level2=pygame.Rect(90,85,150,50)
            self.level3=pygame.Rect(90,145,150,50)
            self.level4=pygame.Rect(90,205,150,50)
            self.level5=pygame.Rect(90,265,150,50)
            self.back=pygame.Rect(90,325,150,50)
            

        
        #Game Clock & Speed
            self.clock = pygame.time.Clock()
            self.fps = 60


        def draw(self):
            self.screen.fill((0, 0, 255))
            self.screen.blit(self.bg, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        def level_loop(self):
            back=False
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type==pygame.MOUSEBUTTONUP:
                        mouse_pos=pygame.mouse.get_pos()
                        if self.level1.collidepoint(mouse_pos):
                            instance=game.Game(1)
                            instance.game_loop()
                            print("level 1")
                        elif self.level2.collidepoint(mouse_pos):
                            instance=game.Game(2)
                            instance.game_loop()
                            print("level 2")
                        elif  self.level3.collidepoint(mouse_pos):
                            instance=game.Game(3)
                            instance.game_loop()
                            print("level 3")
                        elif  self.level4.collidepoint(mouse_pos):
                            instance=game.Game(4)
                            instance.game_loop()
                            print("level 4")
                        elif  self.level5.collidepoint(mouse_pos):
                            instance=game.Game(5)
                            instance.game_loop()
                            print("level 5")
                        elif  self.back.collidepoint(mouse_pos):
                            back=True
                if back: break
                self.draw()


class Scores:
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("Protect The Hive")
            self.screen = pygame.display.set_mode((696, 528))
            self.bg = pygame.transform.scale(load_sprite("scoresbg"), (696, 528))
            self.small_font = pygame.font.Font('freesansbold.ttf', 15)
            self.big_font=pygame.font.Font('freesansbold.ttf', 24)
            self.heading=self.big_font.render("Highscores", True, (85,69,15))
            self.text = []
            self.display=[]
            self.rects=[]
            scores_file=open("scores.txt","r")
            self.back_rect=pygame.Rect(275,444,146,50)
            for line in scores_file:
                current_line=line.split(",")
                self.text+=[current_line[0]]
                self.text+=[current_line[1][:-1]]
                self.text[len(self.text)-1]=int(self.text[len(self.text)-1])
                
            for i in range(1,len(self.text)-2,2):
                for j in range(i, len(self.text),2):
                    print(self.text[i])
                    print(self.text[j])
                    if self.text[i]<self.text[j]:
                        temp=self.text[i]
                        self.text[i]=self.text[j]
                        self.text[j]=temp
                        temp=self.text[i-1]
                        self.text[i-1]=self.text[j-1]
                        self.text[j-1]=temp
            self.num_scores=len(self.text)
            if self.num_scores>20:self.num_scores=20
            for i in range(self.num_scores):
                temp=self.small_font.render(str(self.text[i]), True, (85,69,15))
                self.display+=[temp]
                if i%2==0:
                    self.rects+=[temp.get_rect(topleft=(122,100+i*15))]
                else:
                    self.rects+=[temp.get_rect(topright=(575,100+(i-1)*15))]
                    
       
            #Game Clock & Speed
            self.clock = pygame.time.Clock()
            self.fps = 60


        def draw(self):
            self.screen.fill((0, 0, 255))
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.heading,(282,70))
            for i in range(self.num_scores):
                self.screen.blit(self.display[i],self.rects[i])
            pygame.display.flip()
            self.clock.tick(60)

        def score_loop(self):
             while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type==pygame.MOUSEBUTTONUP:
                        pos=pygame.mouse.get_pos()
                        if self.back_rect.collidepoint(pos):
                            instance=Menu()
                            instance.menu_loop()

                self.draw()




