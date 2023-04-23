
''' IMPORTS '''
# import pygame
import pygame
# import utils for sprites and sounds
from utils import load_sprite, load_sound, print_text
# import menu
import menu
# import game objects
from Objects import Bee, Lives, Enemy, Bullets, Stinger, Barrier, Projectile, Extra, Jellies
# import random 
import random as rnd
from random import choice, randint
# import pygame vectors
from pygame.math import Vector2
# import the scoreboard menu
from highscore import HighScore

''' GAME PARAMETERS '''
# player parameters
LIVES = 3
ENEMIES = 10
SHOOT_CD = 1000 
SOUND = False

# enemy projectile chances
CHANCE_ANT =  0.5 * 0.001
CHANCE_BIRD = 1.2 * 0.01
CHANCE_BEAR = 2 * 0.001

# spawn parameters
ENEMY_Y0 = 25 # initial y position


#implemented by Jared Rodrigues with code integrating the Jellies class and multiple bullet types by Tiaan Mouton
''' MAIN GAME CLASS '''
class Game:

    # Initiate pygame
    def __init__(self, level = 1):
        # Initiate 
        self.__init__pygame()
        pygame.mixer.fadeout(1000)
        bg_music = pygame.mixer.Sound("Assets\Retro_Funk.wav")
        bg_music.play(loops = -1) 
        # Set Resolution
        self.screen = pygame.display.set_mode((800, 600))
        # Set Background Image
        self.background = pygame.transform.scale(load_sprite("newBG"), (800, 600))

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
        # Bullet Type
        self.BulletType = 0
        # Projectiles ( Bullets, Ant Food, Bird Drops, and Bear Honey )
        self.Bullets = []
        self.Projectiles = []
        # Barriers
        self.Barriers = [Barrier((100, 430), 0.8), Barrier((300, 430), 0.8), Barrier((500, 430), 0.8), Barrier((700, 430), 0.8)]
        # Jellies
        self.Jellies = []
        # Enemy arrays 
        self.Boss = pygame.sprite.GroupSingle() # self.Boss
        self.Enemies = pygame.sprite.Group() # self.Enemies
        self.enemy_direction = 2
        # Extra setup
        self.extra = pygame.sprite.Group()
        self.extra_spawn_time = randint(30,80)

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
                # self.extra.update()
                # self.Enemies.update(self.enemy_direction)
                # self.enemy_move_update()
                # self.flying_bird_spawner()
                self.draw() 
                
                # draw and update to screen
                self.Levels() 
                # check level, win, loose


                if self.Endless:
                    self.Endless_process()
            else:
                self.pause_menu()
                self.draw()
    

    ''' PAUSE MENU METHOD '''
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
                    pygame.mixer.fadeout(1000)
                    instance=menu.Menu()
                    instance.menu_loop()
                elif event.key==pygame.K_q:
                    self.pause=False
                    pygame.quit()
                    exit()
        

    ''' LEVELS AND LEVEL METHOD '''
    # Win / Loose / Level System 
    def Levels(self):
        if len(self.Enemies) == 0 and (len(self.Boss) == 0 or self.level_count != 6):
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
                case 6 : 
                    print("Boss Battle passed")
                    print("You Win")
                    self.Win()

                    # Trigger Score here 

                    if keys[pygame.K_SPACE] and len(self.Bullets) < 2:
                    
                        self.message = ""
                        pygame.mixer.fadeout(1000)
                        instance=menu.Menu()
                        instance.menu_loop()

  
    """ LEVELS """

    # hard coded and customizable levels
    def Level_1(self):
        # Level Parameters
        Number_of_Lives = 3
        # reset lives
        self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        self.Barriers = [Barrier((400, 430), 0.8)]
        # spawn enemies
        self.enemy_setup(rows = 5, cols = 10, type = 0)

    def Level_2(self):
        # Level Parameters
        if len(self.Lives) == 0:
            Number_of_Lives = 3
            # reset lives & barriers
            self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        self.Barriers = [Barrier((100, 430), 0.8), Barrier((500, 430), 0.8)]
        # spawn enemies
        self.enemy_setup(rows = 4, cols = 10, type = 0)
        self.enemy_setup(rows = 4, cols = 10, type = 0, y_offset=-200)

    def Level_3(self):
        # Level Parameters
        if len(self.Lives) == 0:
            Number_of_Lives = 3
            # reset lives & barriers
            self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        self.Barriers = [Barrier((100, 430), 0.8), Barrier((500, 430), 0.8)]
        # spawn enemies
        self.enemy_setup(rows = 2, cols = 10, type = 0, y_offset=180)
        self.enemy_setup(rows = 3, cols = 8, type = 0, y_offset=10, x_offset = 130)
        self.enemy_setup(rows = 2, cols = 10, type = 0, y_offset=-120)
        self.enemy_setup(rows = 3, cols = 8, type = 0, y_offset=-280, x_offset = 130)

    def Level_4(self):
        # Level Parameters
        if len(self.Lives) == 0:
            Number_of_Lives = 3
            # reset lives & barriers
            self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        self.Barriers = [Barrier((100, 430), 0.8), Barrier((500, 430), 0.8)]
        # spawn enemies
        self.enemy_setup(rows = 3, cols = 10, type = 0, y_offset=100)
        self.enemy_setup(rows = 2, cols = 6, type = 1, y_offset=-20, x_offset = 180)
        self.enemy_setup(rows = 3, cols = 10, type = 0, y_offset=-180)
        
    def Level_5(self):
        # Level Parameters
        if len(self.Lives) == 0:
            Number_of_Lives = 3
            # reset lives & barriers
            self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        self.Barriers = [Barrier((100, 430), 0.8), Barrier((500, 430), 0.8)]
        # spawn enemies
        self.enemy_setup(rows = 1, cols = 6, type = 1, y_offset=170, x_offset = 180)
        self.enemy_setup(rows = 3, cols = 10, type = 0, y_offset=10)
        self.enemy_setup(rows = 1, cols = 6, type = 1, y_offset=-60, x_offset = 180)
        self.enemy_setup(rows = 3, cols = 10, type = 0, y_offset=-220)
        self.enemy_setup(rows = 1, cols = 6, type = 1, y_offset=-300, x_offset = 180)
        

    def Level_Boss(self):
        # Level Parameters
        if len(self.Lives) == 0:
            Number_of_Lives = 4
            self.Lives = [Lives((40 + 55*i, 550)) for i in range(Number_of_Lives)]
        self.enemy_setup(rows = 1, cols = 1, type = 2, y_offset=30, x_offset = 100)
        

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
        text.append(font.render(f"Invaders : {len(self.Enemies)}", True, (0, 0, 0)))
        text.append(font.render(f"Invaders : {len(self.Enemies)}", True, (250, 0, 0)))
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

    ''' PRE PROCESSING AND USER INPUT '''

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
    

    ''' ALL COLLISION CHECKS '''

    def collision_checks(self):

        # Player Collisions
        # with Enemy 
        for enemy in self.Enemies:
            try :
                if enemy.collider(self.Bee):
                    try: self.Lives.pop(len(self.Lives) - 1) ; self.Bee.hitPoints -= 1;  self.Enemies.remove(enemy)
                    except : pass
            except: pass
        # with Jellies
        for jelly in self.Jellies:
            if self.Bee.collider(jelly):
                jellyUP = Jellies.Collect(jelly)
                self.JellyUPS(jellyUP)
                self.Jellies.remove(jelly)

        # Player Bullet Collisions  
        if self.Bullets:
            for Bullet in self.Bullets:
                
                # Window Collisions
                if not self.screen.get_rect().collidepoint(Bullet.pos):
                    self.Bullets.remove(Bullet)
                
				# Enemy Collisions
                for enemy in self.Enemies:
                    # with bullet
                    if Bullet.collider(enemy):
                        enemy.hitpoints -= Bullet.hitPoints
                        if enemy.hitpoints <= 0:
                            self.Enemies.remove(enemy)
                            # Spawn Jellies (randomly)
                            if Jellies.Spawn():
                                self.Jellies.append(Jellies(enemy.pos))
                        try : self.Bullets.remove(Bullet)
                        except : pass
                        self.score += 1
                    # enemy window 
                    if not self.screen.get_rect().collidepoint(enemy.pos):
                        try: self.Bullets.remove(enemy)
                        except: pass
                    

				# Extra flying bird Collision
                for bird in self.extra:
                    if Bullet.collider(bird):
                        bird.hitpoints -= 1
                        if bird.hitpoints <= 0:
                            self.extra.remove(bird)
                            # Spawn Jellies (always)
                            self.Jellies.append(Jellies(bird.pos))
                        try :self.Bullets.remove(Bullet)
                        except : pass
                        self.score += 1

                # Boss Collision 
                if self.Boss:
                    if Bullet.collider(self.Boss.sprite):
                        self.Boss.sprite.hitpoints -= 1
                        try: self.Bullets.remove(Bullet)
                        except: pass
                        if self.Boss.sprite.hitpoints <= 0:
                            self.Boss.remove(self.Boss.sprite)
                            self.score += 300

                # Barrier Collisions
                for barr in self.Barriers:
                    if barr.collider(Bullet):
                        if barr.hitPoints != 0:
                            try: self.Bullets.remove(Bullet)
                            except: pass
                            barr.update_damage()
                        else: 
                            self.Barriers.remove(barr)
                            self.Bullets.remove(Bullet)

        # Enemy Bullet Collisions

        if self.Projectiles:
            for proj in self.Projectiles:
                
                # Window Collisions
                if not self.screen.get_rect().collidepoint(proj.pos):
                    self.Projectiles.remove(proj)

                # Barrier Collisions
                for barr in self.Barriers:
                    if barr.collider(proj):
                        if barr.hitPoints != 0:
                            self.Projectiles.remove(proj)
                            barr.update_damage()
                        else: 
                            self.Barriers.remove(barr)
                            self.Projectiles.remove(proj)

                # Player Collisions

                if proj.collider(self.Bee):
                    try: self.Lives.pop(len(self.Lives) - 1) ; self.Bee.hitPoints -= 1 ;  self.Projectiles.remove(proj)
                    except : pass



    ''' MOVEMENT / COMBAT'''
    # Process Movement & Combat
    def process(self):

        # Attacks 
        for enemy in self.Enemies:
            rand = rnd.randint(0, int(1/CHANCE_ANT)) # chance of shooting 1/5000
            if rand == 1:
                self.enemy_shoot(enemy.pos, enemy.type)

        for bird in self.extra:
            rand = rnd.randint(0, int(1/CHANCE_BIRD))
            if rand == 1:
                self.enemy_shoot(bird.pos, 1)

        if self.Boss:
            rand = rnd.randint(0, int(100))
            if rand == 1:
                self.enemy_shoot(self.Boss.sprite.pos, 3)
            self.boss_summon()

        # MOVEMENT

        # Process Bee Movements
        self.Bee.move()
        self.Stinger.move(self.Bee)

        # Enemy Movement 

        self.extra.update()
        self.Enemies.update(self.enemy_direction)
        self.Boss.update(self.enemy_direction)
        self.boss_move_update()
        self.enemy_move_update()
        self.flying_bird_spawner()

        # Process all Bullet Movement 
        for bull in self.Bullets:
            try : bull.move()
            except : pass

        # Enemy Projectile movement 
        for proj in self.Projectiles:
            try : proj.move()
            except : pass

        # Jelly movement
        for jell in self.Jellies:
            if self.Barriers != []:
                for barr in self.Barriers:
                    if not jell.collider(barr):
                        try : jell.move()
                        except : pass
            else:
              try : jell.move()
              except : pass  

        # COLLISIONS
        self.collision_checks()
        
        # Check if out of lives
        if self.Bee.hitPoints == 0:
            
            if self.TextCD < 2000:
                self.message = "You Loose!"
                self.TextCD += self.clock.get_time()
                
            elif self.TextCD < 4000:
                self.message = "Unlucky! Better luck next time :)"
                self.TextCD += self.clock.get_time()
            else: 
                pygame.quit()
                instance = HighScore(self.score)
                instance.score_loop()

    def Endless_Process(self):
        pass

    ''' UPDATE TO SCREEN DRAW METHOD '''
    def draw(self):
        # Fill Screen and Draw Background
        self.screen.fill((0, 0, 255))
        self.screen.blit(self.background, (0, 0))

        # Draw Enemy Sprites
        self.Enemies.draw(self.screen)
        self.extra.draw(self.screen)

        # Draw Player Sprites
        self.Stinger.draw(self.screen)
        self.Bee.draw(self.screen)
        
        # Draw Obstacles
        for barr in self.Barriers:
            barr.draw(self.screen)

        # Draw Boss
        if self.Boss:
            self.Boss.draw(self.screen)
            # Draw Boss Health Bar
            pygame.draw.rect(self.screen, (10,10,10), (self.Boss.sprite.rect[0] + 50, self.Boss.sprite.rect[1]- 10, 150, 10)) 
            pygame.draw.rect(self.screen, (128,0,0), (self.Boss.sprite.rect[0] + 50, self.Boss.sprite.rect[1] - 10, 150 - (3 * (50 - self.Boss.sprite.hitpoints)), 10))

        # Draw Lives
        for life in self.Lives:
            life.draw(self.screen)

        # Draw Player Bullets
        for bullet in self.Bullets:
            bullet.draw(self.screen)

        # Draw Enemy Bullets
        for proj in self.Projectiles:
            proj.draw(self.screen)

        # Draw Jellies   
        for jelly in self.Jellies:
            jelly.draw(self.screen)

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
    




    ''' ENEMY METHODS '''

    def enemy_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 20, type = 0):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                Enemy_sprite = Enemy(type,x,y)
                
                if type != 2:
                    self.Enemies.add(Enemy_sprite)
                else: 
                    self.Boss.add(Enemy_sprite)
                

    def enemy_move_update(self):
        all_enemies = self.Enemies.sprites()
        for enemy in all_enemies:
            if enemy.rect.right >= 800:
                self.enemy_direction = -1
                self.enemy_move_down(8)
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(8)

    def boss_move_update(self):
        if self.Boss:
            boss = self.Boss.sprite
            if boss.rect.right >= 800:
                    self.enemy_direction = -1
            elif boss.rect.left <= 0:
                    self.enemy_direction = 1

    def boss_summon(self):
        if len(self.Enemies) == 0:
            ran = rnd.randint(0,100)
            if ran < 60:
                self.enemy_setup(1,8,60,40,self.Boss.sprite.pos[0] -200,300,0)
            else: 
                self.enemy_setup(1,5,60,40,self.Boss.sprite.pos[0] - 120,300,1)

    def enemy_move_down(self,distance):
        if self.Enemies:
            for enemy in self.Enemies.sprites():
                enemy.rect.y += distance

    def flying_bird_spawner(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),800))
            self.extra_spawn_time = randint(300,700)

    #powerups
    def JellyUPS(self, jelly):
        match (jelly):
            case 0:
                if self.BulletType != 0:
                    self.BulletType = 0
                else:
                    self.score = 3
            case 1:
                if self.BulletType != 1:
                    self.BulletType = 1
                else:
                    self.score += 2
            case 2:
                if self.BulletType != 2:
                    self.BulletType = 2
                else:
                    self.score += 2
            case 3:
                self.score += 7
            case 'h':
                if self.Bee.hitPoints < 3:
                    self.Bee.hitPoints +=1
                    self.Lives.append(Lives((40 + 55*len(self.Lives), 550)))
                else:
                    self.score += 10
            case 'b':
                for j in self.Barriers:
                    if j.hitPoints < 4:
                        j.hitPoints += 2
                        j.update_damage()
                    else:
                        self.score += 10






    ''' SHOOT FUNCTION FOR BEE '''
    def shoot(self):
        # print(self.Bee.direction)  
        #self.ShootSound.play() # tis a terrible sound
        self.Bullets.append(Bullets(self.Bee.pos, self.Bee.aim(), self.Bee.direction.angle_to(self.Bee.aim()), self.BulletType))
    
    ''' ENEMY SHOOT FUNCTION'''
    def enemy_shoot(self, pos, type = 0):
        self.Projectiles.append(Projectile(position = pos, velocity = Vector2(0,1),type = type))
    
    ''' SUMMON FUNCTION FOR BEARS and ENDLESS MODE '''
    def summon(self):
        pass

