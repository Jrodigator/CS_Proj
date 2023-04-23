import pygame
import menu
from utils import load_sprite
from sys import exit
from outstream import OutStream

#Implemented by John Cokayne 25863878 with a few lines by Jared Rodrigues and Tiaan Mouton
class Leaderboard:
        #initialises all the components of the leaderboard screen
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("Protect The Hive")
            #checks if music is playing. if not, starts playing Retro_platforming.wav
            if not pygame.mixer.get_busy():
                bg_music = pygame.mixer.Sound("Assets\Retro_Platforming.wav")
                bg_music.play(loops = -1)
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
            #reads the contents of scores.txt into the self.txt array, where the even indexes stores the players name, and the odd indexes store the players score 
            for line in scores_file:
                current_line=line.split(",")
                print(current_line)
                self.text+=[current_line[0]]
                self.text+=[current_line[1]]
                self.text[len(self.text)-1]=int(self.text[len(self.text)-1])

            scores_file.close()
            #sorts the players in desceneding order of score
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
            #ensures the max number of scores to be displayed is 10
            if self.num_scores>20:self.num_scores=20
            self.display += [self.small_font.render('', True, (85,69,15))] *2
            #renders the top player names and their scores and stores them in the self.display array. also creates rects for these scores and names that are in the right places
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

#displays the leaderboard screen
        def draw(self):
            self.screen.fill((0, 0, 255))
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.heading,(282,70))
            for i in range(self.num_scores):
                self.screen.blit(self.display[i],self.rects[i])
            pygame.display.flip()
            self.clock.tick(60)
#loops while the user is on the score screen
        def score_loop(self):
             while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    #checks if the user clicks the back button and takes the user back to the main menu if they do
                    if event.type==pygame.MOUSEBUTTONUP:
                        pos=pygame.mouse.get_pos()
                        if self.back_rect.collidepoint(pos):
                            instance= menu.Menu()
                            instance.menu_loop()

                self.draw()

#a subclass of leaderboard that is displayed only when a player is entering their name to be stored with their score on scores.txt
#Implemented by Tiaan Mouton 26017377
class HighScore(Leaderboard):
    #initialises the object and its parent class, leaderboard
    def __init__(self, score):
        self._score = score

        super().__init__()
        self.draw()

        self.getName()
        self.score_loop()
    #method is responsible for creating the input box for the user to input their name and controlling the length of the name the user may input
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
                    #changes the colour of the textbox to white if the user clicks on it to enter their name, otherwise makes it grey
                    if self.rects[0].collidepoint(event.pos):
                        select = not select
                        select_color = selected
                    else:
                        select = False
                        select_color = unselected
                #if the user has selected the text box and pressed return, saves the name the user entered and the associated score to the scores.txt text file and returns the user to the main menu
                if select:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            print(name)
                            file = open('scores.txt', 'a')
                            file.write('\n' + name.upper() + ',' + str(self._score))
                            file.close()

                            #remains to show it can be done with Outstream
                            #file = OutStream('scores.txt')
                            #file.writeln(name + ',' + str(self._score))
                            
                            instance = menu.Title_Screen()
                            instance.title_loop()
                        #removes a character from the entered name if the user presses backspace
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        #appends an entered character to the name as long as the name is less than 3 characters long
                        else:
                            name += event.unicode
                            if len(name) > 3:
                                name = name[:-1]

                input_box.fill(select_color)
                #displays the highscore screen and its components
                self.screen.blit(input_box, self.rects[0])
                self.display[0] = self.small_font.render(name.upper(), True, (85,69,15))
                self.screen.blit(self.display[0], self.rects[0])
                pygame.display.flip()