import pygame
# import utils for sprites and sounds
from utils import load_sprite, load_sound, print_text
# import game objects
from Objects import Bee, Lives, Enemy, Bullets
import menu
from sys import exit
###########################################################################################################################################

from pygame.math import Vector2

LIVES = 3
ENEMIES = 10
SOUND = False


# ENEMY CLASS
class Game:

    # Initiate pygame
    def __init__(self):
        # Initiate 
        self.__init__pygame()
        # Set Resolution
        self.screen = pygame.display.set_mode((800, 600))
        # Set Background Image
        self.background = pygame.transform.scale(load_sprite("hive"), (900, 600))

        # Game Clock & Speed
        self.clock = pygame.time.Clock()
        self.fps = 60
        # Text and Shot Cooldown 
        self.TextCD = self.clock.get_time()
        self.lastShot = self.clock.get_time()
        # Level Tracker
        self.level_count = 1

        # Create Bee
        self.Bee = Bee((100, 500))
        # Create Lives
        self.Lives = []
        # Bullets
        self.Bullets = []

        # Enemy arrays 
        self.Ant = []
        self.Birds = []
        self.Bears = []

        # Message 
        self.message = ""

        # sounds
        self.AntDieSound = load_sound("FunnyBuzz")
        self.BirdDieSound = load_sound("BirdDeath")
        self.ShootSound = load_sound("shoot")
        self.LifeLossSound = load_sound("LifeLoss") #.set_volume(0.2)
        self.StartLevelSound = load_sound("StartLevel")

        # start level 1
        self.Level_1()

        # pause menu 
        self.pause=False



    # LEVELS
    def Level_1(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 20
        Number_of_Birds = 0

        # Level sound
        if SOUND: 
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
    
        # spawn enemies
        self.Ant = [Enemy((50, 50 - 80*i), 1) for i in range(Number_of_Ants)]

    def Level_2(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 15
        Number_of_Birds = 3

        # Level sound
        if SOUND:
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        
        # spawn enemies
        self.Ant = [Enemy((50, 50 - 80*i), 1) for i in range(Number_of_Ants)]
        self.Birds = [Enemy((50 , 50 - 80*Number_of_Ants/2 - 75*i), 2) for i in range(Number_of_Birds)]
        self.Ant.append(Enemy((50, 50 - 80*Number_of_Ants/2 - 80*Number_of_Birds - 80*i), 1) for i in range(Number_of_Ants)) 

    def Level_3(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 20
        Number_of_Birds = 10
        
        # Level sound
        if SOUND:
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        
        # spawn enemies
        self.Ant = [Enemy((50, 50 - 75*i), 1) for i in range(Number_of_Ants)]
        self.Birds = [Enemy((50 , 50 - 75*i), 2) for i in range(Number_of_Birds)]
        pass

    def Level_4(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 25
        Number_of_Birds = 15

        # Level sound
        if SOUND: 
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        
        # spawn enemies
        self.Ant = [Enemy((50, 50 - 75*i), 1) for i in range(Number_of_Ants)]
        self.Birds = [Enemy((50 , 50 - 75*i), 2) for i in range(Number_of_Birds)]
        pass

    def Level_5(self):
        # Level Parameters
        Number_of_Lives = 5
        Number_of_Ants = 0
        Number_of_Birds = 0
        
        # Level sound
        if SOUND:
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        
        # spawn enemies
        self.Ant = [Enemy((50, 50 - 75*i), 1) for i in range(Number_of_Ants)]
        self.Birds = [Enemy((50, 50 - 75*i), 2) for i in range(Number_of_Birds)]
        self.Bears = [Enemy((400, 300), 3)]
        pass

    def Level_Bonus(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 20
        Number_of_Birds = 0

        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]

        self.Ant = [Enemy((50, 50 - 75*i), 1) for i in range(Number_of_Ants)]
        self.Birds = [Enemy((50 + 75*i, 50), 2) for i in range(Number_of_Birds)]
        self.Bears = [Enemy((50 + 75*i, 50), 1) for i in range(ENEMIES)]
        pass

    # Main game loop
    def game_loop(self,level=1):
        self.level_count=level
        while True:
            self.read() # read input
            self.process() # process input
            self.draw() # draw to screen
            self.Levels() # check level, win, loose
            print(len(self.Ant))
            

    # Win / Loose / Level System 
    def Levels(self):
        if (len(self.Ant) == 0) and (len(self.Birds) == 0):
            
            keys = pygame.key.get_pressed()
            match self.level_count: 
                case 1 : 
                    print("level 1 passed")
                    self.message = "Level 1 Passed! Press Space to continue"

                    if keys[pygame.K_SPACE]:
                    # Level passed * text
                        self.Level_2()
                        self.level_count += 1
                        self.message = ""

                case 2 : 
                    print("level 2 passed")
                    self.message = "Level 2 Passed! Press Space to continue"

                    if keys[pygame.K_SPACE]:
                    # Level passed * text
                        self.Level_3()
                        self.level_count += 1
                        self.message = ""
                case 3 : 
                    print("level 3 passed")
                    self.message = "Level 3 Passed! Press Space to continue"

                    if keys[pygame.K_SPACE]:
                    # Level passed * text
                        self.Level_4()
                        self.level_count += 1
                        self.message = ""
                case 4 :
                    print("level 4 passed")
                    self.message = "Level 4 Passed! Press Space to continue"

                    if keys[pygame.K_SPACE]:
                    # Level passed * text
                        self.Level_5()
                        self.level_count += 1
                        self.message = ""
                case 5 :
                    print("level 5 passed")
                    self.message = "Level 5 Passed! Press Space to continue"

                    if keys[pygame.K_SPACE]:
                    # Level passed * text
                        self.Win()
                        self.level_count += 1
                        self.message = ""
    
    def Win(self):
        self.message = "You Won!"
        

    # Initiate Game Window
    def __init__pygame(self):
        pygame.init()
        pygame.display.set_caption("Hive Invaders")
    
    # for all text
    def text(self):
        font = pygame.font.Font('freesansbold.ttf', 16)
        
        # list of texts
        text = []
        # list of their size 
        textRect = []
        
        # Always Rendered Text 
        text.append(font.render("Use (W, A, S, D) or the Arrow Keys to Move", True, (0, 0, 0)))
        text.append(font.render("Use Space or Mouse Button to Shoot.", True, (0,0,0)))
        
        font = pygame.font.Font('freesansbold.ttf', 24)

        # # Level Text 
        # text.append(font.render("Starting Level 1", True, (255, 0, 0)))     # 2 -> 11
        # text.append(font.render("Level 1 Complete !", True, (255, 0, 0)))
        # text.append(font.render("Starting Level 2", True, (255, 0, 0)))
        # text.append(font.render("Level 2 Complete !", True, (255, 0, 0)))
        # text.append(font.render("Starting Level 3", True, (255, 0, 0)))
        # text.append(font.render("Level 3 Complete !", True, (255, 0, 0)))
        # text.append(font.render("Starting Level 4", True, (255, 0, 0)))
        # text.append(font.render("Level 4 Complete !", True, (255, 0, 0)))
        # text.append(font.render("Starting Level 5", True, (255, 0, 0)))
        # text.append(font.render("Level 5 Complete !", True, (255, 0, 0)))

        # # WIN LOOSE 

        # text.append(font.render("YOU WON THE GAME !", True, (255, 0, 0)))  # 12 -> 15
        # text.append(font.render("Now for the real challenge ;)", True, (255, 0, 0)))
        # text.append(font.render("Starting Bonus level : infinite", True, (255, 0, 0)))
        # text.append(font.render("You Lost! Unlucky! Better luck next time", True, (255, 0, 0)))
        
        for i in range(2):
            textRect.append(text[i].get_rect())
        
        # set position
        textRect[0].center = (170, 10)
        textRect[1].center = (150, 30)

        return text, textRect

    # Process input & Calculate Movement
    def read(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            ## BEE
        # Reset velocity
        self.Bee.velocity = Vector2(0, 0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.Bee.velocity += Vector2(3, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.Bee.velocity += Vector2(-3, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.Bee.velocity += Vector2(0, -1.5)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.Bee.velocity += Vector2(0,1.5)
        if keys[pygame.K_p]:
            self.pause=True

        # Bee Shoot
        self.lastShot += self.clock.get_time()
            
        if self.lastShot > 200:
            self.lastShot = 0

        if self.lastShot == 0 and (keys[pygame.K_SPACE] or keys[pygame.MOUSEBUTTONDOWN] > 0):
            self.shoot()
                


            ## ENEMY 
        # self.Ant.velocity = Vector2(0)
        for ant in self.Ant:
            ant.AIMove()  

        for bird in self.Birds:
            bird.AIMove()

    # Process Movement & Combat
    def process(self):

            # MOVEMENT

        # Process Bee Movements
        self.Bee.move()
        
        # Process all Ant Movement
        for ant in self.Ant:
            ant.move()

        # Bird movement 
        for bird in self.Birds:
            bird.move()
        
        # Process all Bullet Movement 
        for bull in self.Bullets:
            bull.move()

            # COLLISIONS

        # Check for Bullet/Window collisions -> delete
        for bullet in self.Bullets:
            if not self.screen.get_rect().collidepoint(bullet.pos):
                self.Bullets.remove(bullet)

        # Check for Ant/Bullet collisions or Ant/Bee collisions -> delete
        for i in self.Ant:

            # Ant Bullet Collision
            for j in self.Bullets:
                if i.collider(j):
                    # play ant death sound
                    if SOUND:
                        self.AntDieSound.play()
                    # remove ant object hit
                    self.Ant.remove(i)
                    # remove bullet that hit
                    self.Bullets.remove(j)
                    
            # Ant Bee Collision
            if i.collider(self.Bee):
                try: self.Lives.pop(len(self.Lives) - 1) ; self.Ant.remove(i)
                except : pass

        # Check for Bird/Bullet collisions or Bird/Bee collisions -> delete
        for i in self.Birds:

            # Bird Bullet Collision
            for j in self.Bullets:
                if i.collider(j):
                    if i.hitpoints == 1:
                        # play Bird death sound
                        if SOUND:
                            self.BirdDieSound.play()
                        # remove Bird object hit
                        self.Birds.remove(i)
                        # remove bullet that hit
                        self.Bullets.remove(j)
                    else: 
                        i.hitpoints -= 1
                        self.Bullets.remove(j)
                    
            # Bird Bee Collision
            if i.collider(self.Bee):
                try: self.Lives.pop(len(self.Lives) - 1) ; self.Birds.remove(i)
                except : pass

        
        

        # Check if out of lives
        if len(self.Lives) == 0:
            
            if self.TextCD < 2000:
                self.message = "You Loose!"
                self.TextCD += self.clock.get_time()
                
            elif self.TextCD < 4000:
                self.message = "Unlucky! Better luck next time :)"
                self.TextCD += self.clock.get_time()
            else:
                self.Ant=[]
                self.Birds=[]
                self.bears=[]
                self.Bullets=[]
                instance = menu.Menu()
                instance.game_loop()
        
        if self.pause:
            self.pause_menu()
                
    def draw(self):
        self.screen.fill((0, 0, 255))
        self.screen.blit(self.background, (0, 0))

        self.Bee.draw(self.screen)
        if self.Bears:
            self.Bears[0].draw(self.screen)
        for ant in self.Ant:
            ant.draw(self.screen)

        for bird in self.Birds:
            bird.draw(self.screen)
        

        for life in self.Lives:
            life.draw(self.screen)

        for bullet in self.Bullets:
            bullet.draw(self.screen)

        # Static Text 
        for i in range(2):
            self.screen.blit(self.text()[0][i], self.text()[1][i])

        # Dynamic Text
        if self.message: 
            print_text(self.screen, self.message)
            


        
        pygame.display.flip()
        
        self.clock.tick(60)

    def shoot(self):
        # print(self.Bee.direction)  

        #self.ShootSound.play() # tis a terrible sound
        self.Bullets.append(Bullets(self.Bee.pos, self.Bee.aim(), self.Bee.direction.angle_to(self.Bee.aim())))
        
    def summon(self):
        # self.Ant.append()
        pass

    def pause_menu(self):
        pause_text="Pause. Press 'P' to unpause, 'M' to go to menu, 'Q' to quit"
        while True:
            print_text(self.screen, pause_text)
            keys=pygame.key.get_pressed()
            if keys[pygame.K_p]:
                #self.message=""
                break
            elif keys[pygame.K_m]:
                instance=menu.Menu()
                instance.menu_loop()
                break
            elif keys[pygame.K_q]:
                pygame.quit()
                exit()
            self.clock.tick(60)
                
        