# vectors from pygame math module
from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame.mouse import get_pos as gp 
# import sprite manager
from utils import load_sprite, load_sound
import random as r 
import math

BULLETSPEED = 5
ANT_SPEED = 3


UP = Vector2(0, -1)

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def getAngle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (len(v1) * len(v2)))

class GameObject:
    def __init__(self, position, sprite, velocity, Hp = 1):
        self.pos = Vector2(position)
        self.sprite = sprite
        self.hitPoints = Hp
        
        #radial hitbox (circle)
        self.hitbox = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.restrictions = (0, 800, 0, 600) # x1, x2, y1, y2 (border restrictions)

    def __del__(self):
        #print("Object has been deleted!")
        pass
    
    def draw(self, screen):
        # center position of the sprite (normalize)
        d_position = self.pos - Vector2(self.sprite.get_width() / 2) # Vector2(self.hitbox)
        # draw from center position 
        screen.blit(self.sprite, d_position)

    def move(self):  

        
        
        # update position with velocity
        self.pos += self.velocity

    def aim(self):
        
        mouse = gp()

        # if Vector2(mouse).y < dir.y : mouse = [mouse[0], dir.y]

        vect = mouse - self.pos
        dist = math.dist(mouse, self.pos) 
        dirVect = vect/dist

        if mouse[1] > self.pos.y : 
            dirVect[1] *= -1

        return (dirVect)

    # checks if the object is colliding with another object
    def collider(self, entity):
        distance = self.pos.distance_to(entity.pos)
        return distance < self.hitbox + entity.hitbox


class Bee(GameObject):
    def __init__(self, position):

        self.shoot_sound = load_sound("shoot")
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("Bee"), Vector2(0))
        self.restrictions = (30, 770, 430, 570)

    

    def draw(self, surface):

        angle = self.direction.angle_to(self.aim())
        rotated_surface = rotozoom(self.sprite, -angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.pos - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def move(self):

        # Check if on border and change direction
        #     left border
        if self.pos.x < self.restrictions[0]:
            self.pos.x = self.restrictions[0]
            self.velocity.x *= -1
            # right border
        elif self.pos.x > self.restrictions[1]:
            self.pos.x = self.restrictions[1]
            self.velocity.x *= -1
            # top border
        if self.pos.y < self.restrictions[2]:
            self.pos.y = self.restrictions[2]
            self.velocity.y *= -1

            # bottom border
        elif self.pos.y > self.restrictions[3]:
            self.pos.y = self.restrictions[3]
            self.velocity.y *= -1

        # update position with velocity
        self.pos += self.velocity

class Bullets(GameObject):
    
    def __init__(self, position, velocity, angle, size=0.1):
        self.size = size

        # load sprite
        sprite = load_sprite("bullet")
        # rotate sprite to direction of Bee
        rotatedSprite = rotozoom(sprite, -angle, 1)
        
        super().__init__(position, rotatedSprite, velocity*BULLETSPEED)

        self.hitbox = sprite.get_height() / 6




class Lives(GameObject):
    def __init__(self, position, size=0.4):
        self.size = size
        life = rotozoom(load_sprite("Life"), 0, size)

        super().__init__(position, life, Vector2(0))

# Enemies class -> has a type that affects its sprite, lives and damage
    # 1 - Ant -> 1 Dmg, 1 Hp 
    # 2 - Bird -> 2 Dmg, 2 Hp
    # 3 - Bear -> InstaKill, 10 Hp (Boss Battle)

class Enemy(GameObject):
    def __init__(self, position, type=1): 
        self.size = 0.8
        self.restrictions = [0,900,0,900]

        if type == 1: 
            enemy = rotozoom(load_sprite("Ant"), 180, self.size)
            self.hitpoints = 1
        elif type == 2: 
            enemy = rotozoom(load_sprite("Bird"), 0, self.size)
            self.hitpoints = 3
        elif type == 3: 
            enemy = rotozoom(load_sprite("Bear"), 0, self.size*3)
            self.hitpoints = 10

        super().__init__(position, enemy, Vector2(0, ANT_SPEED))

    def AIMove(self):

        # Track points
        TP = [(50, 50), (750, 50), (750, 125), (50, 125), (50, 200), (750, 200), (750, 275), (50, 275), (50, 350), (750, 350), (750, 425), (50, 425), (50, 500), (750, 500), (750, 550) ]
        
        # Threshold to point (Buggs out if there is no theshold)
        Thresh = 1.5
        
        # AI Movement Track
        if math.dist(self.pos, TP[0]) < Thresh: self.velocity = Vector2(ANT_SPEED, 0); self.pos = Vector2(TP[0])
        if math.dist(self.pos, TP[1]) < Thresh: self.velocity = Vector2(0, ANT_SPEED); self.pos = Vector2(TP[1])
        elif math.dist(self.pos, TP[2]) < Thresh: self.velocity = Vector2(-ANT_SPEED, 0); self.pos = Vector2(TP[2])
        elif math.dist(self.pos, TP[3]) < Thresh: self.velocity = Vector2(0, ANT_SPEED); self.pos = Vector2(TP[3])
        elif math.dist(self.pos, TP[4]) < Thresh: self.velocity = Vector2(ANT_SPEED, 0); self.pos = Vector2(TP[4])
        elif math.dist(self.pos, TP[5]) < Thresh: self.velocity = Vector2(0, ANT_SPEED); self.pos = Vector2(TP[5])
        elif math.dist(self.pos, TP[6]) < Thresh: self.velocity = Vector2(-ANT_SPEED, 0); self.pos = Vector2(TP[6])
        elif math.dist(self.pos, TP[7]) < Thresh: self.velocity = Vector2(0, ANT_SPEED); self.pos = Vector2(TP[7])
        elif math.dist(self.pos, TP[8]) < Thresh: self.velocity = Vector2(ANT_SPEED, 0); self.pos = Vector2(TP[8])
        elif math.dist(self.pos, TP[9]) < Thresh: self.velocity = Vector2(0, ANT_SPEED); self.pos = Vector2(TP[9])
        elif math.dist(self.pos, TP[10]) < Thresh: self.velocity = Vector2(-ANT_SPEED, 0); self.pos = Vector2(TP[10])
        elif math.dist(self.pos, TP[11]) < Thresh: self.velocity = Vector2(0, ANT_SPEED); self.pos = Vector2(TP[11])
        elif math.dist(self.pos, TP[12]) < Thresh: self.velocity = Vector2(ANT_SPEED, 0); self.pos = Vector2(TP[12])