import pygame
import menu
from utils import load_sprite
from sys import exit
from outstream import OutStream

#Implemented by John Cokayne 25863878 with a few lines by Jared Rodrigues and Tiaan Mouton
class Leaderboard:
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
                print(current_line)
                self.text+=[current_line[0]]
                self.text+=[current_line[1]]
                self.text[len(self.text)-1]=int(self.text[len(self.text)-1])

            #scores_file.flush()
            scores_file.close()
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
            self.display += [self.small_font.render('', True, (85,69,15))] *2
            for i in range(self.num_scores):
                temp=self.small_font.render(str(self.text[i]), True, (85,69,15))
                self.display+=[temp]
                if i%2==0:
                    self.rects+=[temp.get_rect(topleft=(122,100+i*15))]
                else:
                    self.rects+=[temp.get_rect(topright=(575,100+(i-1)*15))]
                    
            scores_file.close

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
                            pygame.quit()
                            instance= menu.Menu()
                            instance.menu_loop()

                self.draw()

class HighScore(Leaderboard):
    def __init__(self, score):
        self._score = score

        super().__init__()
        self.draw()

        self.getName()
        self.score_loop()

    def getName(self):
        name = ''
        select = False
        unselected = pygame.Color('Gray')
        selected = pygame.Color('White')
        select_color = unselected

        input_box = pygame.Surface((50, self.small_font.get_height()))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    select_color = selected if select else unselected
                    if self.rects[0].collidepoint(event.pos):
                        select = not select
                        select_color = selected
                    else:
                        select = False
                        select_color = unselected
                
                if select:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            print(name)
                            file = open('scores.txt', 'a')
                            file.write('\n' + name.upper() + ',' + str(self._score))
                            file.close()

                            #file = OutStream('scores.txt')
                            #file.writeln(name + ',' + str(self._score))
                            
                            instance = menu.Title_Screen()
                            instance.title_loop()
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            name += event.unicode
                            if len(name) > 3:
                                name = name[:-1]

                input_box.fill(select_color)

                self.screen.blit(input_box, self.rects[0])
                self.display[0] = self.small_font.render(name.upper(), True, (85,69,15))
                self.screen.blit(self.display[0], self.rects[0])
                pygame.display.flip()