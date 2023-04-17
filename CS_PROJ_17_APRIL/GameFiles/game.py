
''' IMPORTS '''
# import pygame
import pygame
# import utils for sprites and sounds
from utils import load_sprite, load_sound, print_text
# import menu
import menu
# import game objects
from Objects import Bee, Lives, Enemy, Bullets, Stinger, Barrier, Projectile
# import random 
import random as rnd
# import pygame vectors
from pygame.math import Vector2

''' GAME PARAMETERS '''
# player parameters
LIVES = 3
ENEMIES = 10
SHOOT_CD = 500
SOUND = False

# enemy projectile chances
CHANCE_ANT =  1 * 0.001
CHANCE_BIRD = 1.2 * 0.001
CHANCE_BEAR = 2 * 0.001

# spawn parameters
ENEMY_Y0 = 25 # initial y position


''' MAIN GAME CLASS '''
class Game:

    # Initiate pygame
    def __init__(self, level = 1):
        # Initiate 
        self.__init__pygame()
        # Set Resolution
        self.screen = pygame.display.set_mode((800, 600))
        # Set Background Image
        self.background = pygame.transform.scale(load_sprite("hive"), (900, 600))

        # Game Clock & Speed (FPS)
        self.clock = pygame.time.Clock()
        self.fps = 60
        # Text and Shot Cooldown Trackers 
        self.TextCD = self.clock.get_time()
        self.lastShot = self.clock.get_time()
        # Level Tracker
        self.level_count = level - 1
        self.Endless = False 
        # Score Tracker
        self.score = 0

        # Create Bee
        self.Bee = Bee((100, 500))
        # Create Stinger
        self.Stinger = Stinger((100, 500))
        # Create Lives
        self.Lives = []
        # Projectiles ( Bullets, Ant Food, Bird Shits, and Bear Honey )
        self.Bullets = []
        self.Projectiles = []
        # Barriers
        self.Barriers = [Barrier((100, 430), 0.8), Barrier((300, 430), 0.8), Barrier((500, 430), 0.8), Barrier((700, 430), 0.8)]

        # Enemy arrays 
        self.Ant = []
        self.Birds = []
        self.Bears = []

        # Message 
        self.message = ""

        # Sounds
        self.AntDieSound = load_sound("FunnyBuzz")
        self.BirdDieSound = load_sound("BirdDeath")
        self.ShootSound = load_sound("shoot")
        self.LifeLossSound = load_sound("LifeLoss") #.set_volume(0.2)
        self.StartLevelSound = load_sound("StartLevel")

        #self.level_count = 0#startLevel 
        self.Levels()

        # pause menu 
        self.pause=False


    ''' GAME WINDOW '''
    # Initiate Game Window
    def __init__pygame(self):
        pygame.init()
        pygame.display.set_caption("Hive Invaders")
    
    ''' MAIN GAME LOOP '''
    def game_loop(self):
        while True:
            if not self.pause:
                self.read() 
                # read input & pre process (calculate)
                self.process() 
                # process input, detect collisions, etc
                self.draw() 
                # draw and update to screen
                self.Levels() 
                # check level, win, loose
                if self.Endless:
                    self.Endless_process()
            else:
                self.pause_menu()
                self.draw()
    


    # Win / Loose / Level System 
    def Levels(self):
        if (len(self.Ant) == 0) and (len(self.Birds) == 0):
        # Level only to be increased if all enemies are dead 
            
            keys = pygame.key.get_pressed()
            # Get events method returning a list of keys pressed

            match self.level_count :
                case 0 : 
                    self.message = "Starting Level 1 - Press Space to continue"
                    if keys[pygame.K_SPACE]:
                        self.Level_1()
                        self.level_count += 1
                        self.message = ""

                case 1 : 
                    #print("level 1 passed")
                    self.message = "Starting Level 2 - Press Space to continue"

                    if keys[pygame.K_SPACE] and len(self.Bullets) < 2:
                    # Level passed * text
                        self.Level_2()
                        self.level_count += 1
                        self.message = ""
            
                case 2 : 
                    print("level 2 passed")
                    self.message = "Starting Level 3 - Press Space to continue"

                    if keys[pygame.K_SPACE] and len(self.Bullets) < 2:
                    # Level passed * text
                        self.Level_3()
                        self.level_count += 1
                        self.message = ""

                case 3 : 
                    print("level 3 passed")
                    self.message = "Starting Level 4 - Press Space to continue"

                    if keys[pygame.K_SPACE] and len(self.Bullets) < 2:
                    # Level passed * text
                        self.Level_4()
                        self.level_count += 1
                        self.message = ""

                case 4 :
                    print("level 4 passed")
                    self.message = "Starting Level 5 - Press Space to continue"

                    if keys[pygame.K_SPACE] and len(self.Bullets) < 2:
                    # Level passed * text
                        self.Level_5()
                        self.level_count += 1
                        self.message = ""

                case 5 :
                    print("level 5 passed")
                    self.message = "Starting Boss Battle - Press Space to continue"

                    if keys[pygame.K_SPACE] and len(self.Bullets) < 2:
                    # Level passed * text
                        self.Level_Boss()
                        self.level_count += 1
                        self.message = ""

                case _: 
                    print("You Win")
                    print("endless time")

                    self.message = "ENDLESS MODE - Press Space to continue"
                    if keys[pygame.K_SPACE] and len(self.Bullets) < 2:
                    # Level passed * text
                        self.Level_Endless()
                        self.Endless = True
                        self.message = ""

    """ LEVELS """

    # hard coded and customizable levels
    def Level_1(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 20
        Number_of_Birds = 0
        Row_Step = 80 # MULTIPLES OF 60 ( ie. 60 x number of unique enemies )
        Waves = 4
    
        # Level sound
        if SOUND: 
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]

        self.Barriers = [Barrier((400, 430), 0.8)]

        

        # spawn enemies
        for j in range(Waves):
            self.Ant += [Enemy((60 + (round(700/Number_of_Ants))*i, ENEMY_Y0 - j*Row_Step), 1, (-1)**(j + 1)) for i in range(Number_of_Ants)]


    def Level_2(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 10
        Number_of_Birds = 4
        Row_Step = 160 #(80 x 2 unique enemies)
        Waves = 2

        # Level sound
        if SOUND:
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]

        
        self.Barriers = [Barrier((100, 430), 0.8), Barrier((500, 430), 0.8)]
        
        # spawn enemies
        for j in range(Waves):
            self.Ant += [Enemy((60 + (round(700/Number_of_Ants))*i, ENEMY_Y0-j*Row_Step), 1, (-1)**(j*2)) for i in range(Number_of_Ants)]
            self.Birds += [Enemy((60 + (round(700/Number_of_Birds))*i, ENEMY_Y0 - 80 -j*Row_Step), 2, (-1)**(j*2 + 1)) for i in range(Number_of_Birds)]


    def Level_3(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 5
        Number_of_Birds = 6
        Row_Step = 120
        Waves = 3
        
        # Level sound
        if SOUND:
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]

        self.Barriers = [Barrier((100, 430), 0.8), Barrier((400, 410), 0.8), Barrier((700, 430), 0.8)]
        
        # spawn enemies
        for j in range(Waves):
            self.Ant += [Enemy((60 + (round(700/Number_of_Ants))*i, -20-j*Row_Step), 1, (-1)**(j*2)) for i in range(Number_of_Ants)]
            self.Birds += [Enemy((60 + (round(700/Number_of_Birds))*i, -80 -j*Row_Step), 2, (-1)**(j*2 + 1)) for i in range(Number_of_Birds)]

    def Level_4(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 15
        Number_of_Birds = 8
        Row_Step = 120
        Waves = 3

        # Level sound
        if SOUND: 
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]

        self.Barriers = [Barrier((100, 430), 0.6), Barrier((250, 430), 0.6), Barrier((400, 410), 0.6), Barrier((550, 430), 0.6), Barrier((700, 430), 0.6)]
        
        # spawn enemies
        for j in range(Waves):
            self.Ant += [Enemy((60 + (round(700/Number_of_Ants))*i, -80-j*Row_Step), 1, (-1)**(j*2 + 1)) for i in range(Number_of_Ants)]
            self.Birds += [Enemy((60 + (round(700/Number_of_Birds))*i, -20 -j*Row_Step), 2, (-1)**(j*2)) for i in range(Number_of_Birds)]

        pass

    def Level_5(self):
        # Level Parameters
        Number_of_Lives = 5
        Number_of_Ants = 0
        Number_of_Birds = 0
        Waves = 0 
        Row_Step = 0
        
        # Level sound
        if SOUND:
            self.StartLevelSound.play()

        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        

    def Level_Boss(self):
        # Level Parameters
        Number_of_Lives = 3
        Number_of_Ants = 20
        Number_of_Birds = 0

        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]

        self.Ant = [Enemy((50, 50 - 75*i), 1) for i in range(Number_of_Ants)]
        self.Birds = [Enemy((50 + 75*i, 50), 2) for i in range(Number_of_Birds)]
        self.Bears = [Enemy((50 + 75*i, 50), 1) for i in range(ENEMIES)]
        pass

    def Level_Endless(self):
        pass


    
    
    def Win(self):
        self.message = "You Won!"


    """ STATIC TEXT """ # dynamic text function in utils.py
    def text(self):
        font = pygame.font.Font('freesansbold.ttf', 16)
        
        # list of texts
        text = []
        # list of their size 
        textRect = []
        
        # Always Rendered Text 
        text.append(font.render(f"Score : {self.score}", True, (0, 0, 0)))
        text.append(font.render(f"Score : {self.score}", True, (250, 0, 0)))
        text.append(font.render(f"Level : {self.level_count}", True, (0, 0, 0)))
        text.append(font.render(f"Level : {self.level_count}", True, (250, 0, 0)))
        text.append(font.render(f"Invaders : {len(self.Ant) + len(self.Birds)}", True, (0, 0, 0)))
        text.append(font.render(f"Invaders : {len(self.Ant) + len(self.Birds)}", True, (250, 0, 0)))
        text.append(font.render("Use Space or Mouse Button to Shoot.", True, (0,0,0)))
        text.append(font.render("Use Space or Mouse Button to Shoot.", True, (250,0,0)))
        
        font = pygame.font.Font('freesansbold.ttf', 24)

        for i in range(8):
            textRect.append(text[i].get_rect())
        
        # set position
        textRect[0].center = (225, 570)
        textRect[1].center = (226, 571)
        textRect[2].center = (315, 570)
        textRect[3].center = (316, 571)
        textRect[4].center = (415, 570)
        textRect[5].center = (416, 571)
        textRect[6].center = (635, 570)
        textRect[7].center = (636, 571)

        return text, textRect

    ''' PRE PROCESSING AND MOVEMENT CALCUATION '''
    # Process input & Calculate Movement
    def read(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.pause = not self.pause

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

        # Bee Shoot
        self.lastShot += self.clock.get_time()
            
        if self.lastShot > SHOOT_CD:
            self.lastShot = 0

        if self.lastShot == 0 and (keys[pygame.K_SPACE] or keys[pygame.MOUSEBUTTONDOWN] > 0):
            self.shoot()

        ''' ENEMY MOVEMENT '''
        if len(self.Ant) != 0:
            for ant in self.Ant:
                try : ant.newMove()  
                except : pass

        if len(self.Birds) != 0:
            for bird in self.Birds:
                try : bird.newMove()
                except : pass

    # Process Movement & Combat
    def process(self):

            # MOVEMENT

        # Process Bee Movements
        self.Bee.move()
        self.Stinger.move(self.Bee)
        
        # Process all Ant Movement
        for ant in self.Ant:
            rand = rnd.randint(0, int(1/CHANCE_ANT)) # chance of shooting 1/5000
            if rand == 1:
                self.enemy_shoot(ant.pos, 0)
            try : ant.move()
            except : pass

        # Bird movement 
        for bird in self.Birds:
            rand = rnd.randint(0, int(1/CHANCE_BIRD)) # chance of shooting 1/5000
            if rand == 1:
                self.enemy_shoot(bird.pos, 1)
            try : bird.move()
            except : pass

        # Process all Bullet Movement 
        for bull in self.Bullets:
            try : bull.move()
            except : pass

        # other projectile movement 
        for proj in self.Projectiles:
            try : proj.move()
            except : pass

            # COLLISIONS

        # Check for Bullet/Window collisions -> delete
        for bullet in self.Bullets:
            if not self.screen.get_rect().collidepoint(bullet.pos):
                self.Bullets.remove(bullet)
        
        # Check for Projectile/Window collisions -> delete
        for proj in self.Projectiles:
            if not self.screen.get_rect().collidepoint(proj.pos):
                self.Projectiles.remove(proj)

        # Check for Ant/Bullet collisions or Ant/Bee collisions -> delete
        for i in self.Ant:

            # Ant Bullet Collision
            for j in self.Bullets:
                try: 
                    if i.collider(j):
                        # update score 
                        self.score += 1
                        # play ant death sound
                        if SOUND:
                            self.AntDieSound.play()
                        # remove ant object hit
                        self.Ant.remove(i)
                        # remove bullet that hit
                        self.Bullets.remove(j)
                except: pass
                    
            # Ant Bee Collision
            try :
                if i.collider(self.Bee):
                    try: self.Lives.pop(len(self.Lives) - 1) ; self.Ant.remove(i)
                    except : pass
            except: pass

        # Check for Bird/Bullet collisions or Bird/Bee collisions -> delete
        for i in self.Birds:

            # Bird Bullet Collision
            for j in self.Bullets:
                if i.collider(j):
                    if i.hitpoints == 1:
                        # update score 
                        self.score += 3
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

            # projectile Bee Collisions
            for proj in self.Projectiles:
                if proj.collider(self.Bee):
                    try: self.Lives.pop(len(self.Lives) - 1) ; self.Projectiles.remove(proj)
                    except : pass


        # Check for Bullet/Barrier collisions -> delete
        for barr in self.Barriers:
            for bull in self.Bullets:
                if barr.collider(bull):
                    if barr.hitPoints != 0:
                        self.Bullets.remove(bull)
                        barr.update_damage()
                    else: 
                        self.Barriers.remove(barr)
                        self.Bullets.remove(bull)

            for proj in self.Projectiles:
                if barr.collider(proj):
                    if barr.hitPoints != 0:
                        self.Projectiles.remove(proj)
                        barr.update_damage()
                    else: 
                        self.Barriers.remove(barr)
                        self.Projectiles.remove(proj)
        
        

        # Check if out of lives
        if len(self.Lives) == 0 and self.score > 1:
            
            if self.TextCD < 2000:
                self.message = "You Loose!"
                self.TextCD += self.clock.get_time()
                
            elif self.TextCD < 4000:
                self.message = "Unlucky! Better luck next time :)"
                self.TextCD += self.clock.get_time()
            else: 
                pygame.quit()
            
            #pygame.quit()

    def Endless_Process(self):
        pass

    ''' UPDATE TO SCREEN DRAW FUNCTION '''
    def draw(self):
        self.screen.fill((0, 0, 255))
        self.screen.blit(self.background, (0, 0))

        self.Stinger.draw(self.screen)
        self.Bee.draw(self.screen)
        
        for barr in self.Barriers:
            barr.draw(self.screen)

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

        for proj in self.Projectiles:
            proj.draw(self.screen)

        # Static Text 
        for i in range(8):
            self.screen.blit(self.text()[0][i], self.text()[1][i])

        # Dynamic Text
        if self.message: 
            print_text(self.screen, self.message)

        # Pause menu text
        if self.pause==True:
            pause_text="Pause. Press 'P' to unpause, 'M' to go to menu, 'Q' to quit"
            print_text(self.screen, pause_text,24)


        
        pygame.display.flip()
        
        self.clock.tick(60)

    ''' SHOOT FUNCTION FOR BEE '''
    def shoot(self):
        # print(self.Bee.direction)  
        #self.ShootSound.play() # tis a terrible sound
        self.Bullets.append(Bullets(self.Bee.pos, self.Bee.aim(), self.Bee.direction.angle_to(self.Bee.aim())))
    
    ''' ENEMY SHOOR FUNCTION'''
    def enemy_shoot(self, pos, type = 0):
        print("enemy shoot")
        self.Projectiles.append(Projectile(position = pos, velocity = Vector2(0,1),type = type))
    
    ''' SUMMON FUNCTION FOR BEARS and ENDLESS MODE '''
    def summon(self):
        # self.Ant.append()
        pass

    # Pause Menu Function
    def pause_menu(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause=False
                elif event.key == pygame.K_m:
                    self.pause=False
                    instance=menu.Menu()
                    instance.menu_loop()
                elif event.key==pygame.K_q:
                    self.pause=False
                    pygame.quit()
                    exit()
        