# vectors from pygame math module
from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame.mouse import get_pos as gp 
# import sprite manager
from utils import load_sprite, load_sound
import random as r 
import math
from stdrandom import bernoulli

#BULLETSPEED = 8
BULLETSPEED = 20
PROJECTILESPEED = 6
ENEMY_SPEED = 2.8
BEE_SPEED = 1.8
JELLY_SPEED = 12


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
        #self.hitbox = sprite.get_width() / 2
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
    def __init__(self, position, hitpoints):

        self.shoot_sound = load_sound("shoot")
        self.direction = Vector2(UP)
        sprite = load_sprite("Bee")
        super().__init__(position, sprite, Vector2(0), hitpoints)
        self.restrictions = (30, 770, 500, 550)
        self.hitbox = sprite.get_width() / 3

    

    def draw(self, surface):

        angle = self.direction.angle_to(self.aim())
        angle = 180
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
        self.pos += self.velocity*BEE_SPEED

class Stinger(GameObject):
    def __init__(self, position):
        self.direction = Vector2(UP)
        sprite = load_sprite("bull00")
        super().__init__(position, sprite, Vector2(0))
        self.hitbox = sprite.get_width() / 2

    def move(self, Bee):
        self.pos = Bee.pos + (0, -30)

    def draw(self, surface):
        angle = self.direction.angle_to(self.aim())
        rotated_surface = rotozoom(self.sprite, -angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.pos - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
       
class Barrier(GameObject):
    def __init__(self, position, size=1.0):
        self.level = [rotozoom(load_sprite(f"Barrier{i}"), 0, size)for i in range(5)]
        self.size = size
        self.hitbox = load_sprite("Barrier0").get_width() / 4
        barrier = self.level[0]

        super().__init__(position, barrier, Vector2(0), Hp = 4)
    
    def update_damage(self):
        #p = r.randint(0, 2) # 25% chance of taking damage
        #if p == 1:
        self.hitPoints -= 1
        self.sprite = self.level[4 - self.hitPoints]

class Bullets(GameObject):
    
    def __init__(self, position, velocity, angle, type=0):
        #self.size = size

        # load sprite
        if (type == 0): 
            sprite = load_sprite("bull00")
            self.damage = 0.5
            scale = 1
        elif (type == 1): 
            sprite = load_sprite("bull01")
            self.damage = 1
            scale = 1
        elif (type == 2): 
            sprite = load_sprite("bull02")
            self.damage = 1.5
            scale = 0.5
        # rotate sprite to direction of Bee
        rotatedSprite = rotozoom(sprite, -angle, scale)
        self.hitbox = sprite.get_height() / 6

        super().__init__(position, rotatedSprite, velocity*BULLETSPEED, self.damage)

class Projectile(GameObject):
    def __init__(self,  position, velocity, angle = 0, type = 0, size=0.1):
        self.size = size * (type + 1)

        sprite = load_sprite(f"projectile{type}")
        rotatedSprite = rotozoom(sprite, -angle, 1)
        self.hitbox = sprite.get_height() / 6

        super().__init__(position, rotatedSprite, velocity*PROJECTILESPEED)


class Lives(GameObject):
    def __init__(self, position, size=0.4):
        self.size = size
        life = rotozoom(load_sprite("Life"), 0, size)

        super().__init__(position, life, Vector2(0))

# Enemies class -> has a type that affects its sprite, lives and damage
    # 1 - Ant -> 1 Dmg, 1 Hp 
    # 2 - Bird -> 2 Dmg, 3 Hp
    # 3 - Bear -> InstaKill, 10 Hp (Boss Battle)

class Enemy(GameObject):
    def __init__(self, position, type=1, vel = 1): 
        self.size = 0.6
        self.restrictions = [0,900,0,900]
        self.oldPos = position
        self.speed = ENEMY_SPEED

        if type == 1: 
            enemy = rotozoom(load_sprite("Ant"), 180, self.size)
            self.hp = 1
            self.speed += ENEMY_SPEED/2
            self.hitbox = load_sprite("Ant").get_width() / 3
        elif type == 2: 
            enemy = rotozoom(load_sprite("Bird"), 0, self.size)
            self.hp = 3
            self.hitbox = load_sprite("bird").get_width() / 3
        elif type == 3: 
            enemy = rotozoom(load_sprite("Bear"), 0, self.size*3)
            self.hp = 10
            self.hitbox = load_sprite("Bear").get_width() / 2

        super().__init__(position, enemy, vel*Vector2(self.speed, 0), self.hp)

    def newMove(self):
        self.oldPos
        Thresh = 1.5
        LB = 50
        RB = 750 
        Top = 0 
        BottomBound = 800
        yStep = 80 
        if self.pos.x < LB: 
            self.oldPos = self.pos
            self.pos = Vector2(LB + 2, self.pos.y) 
            self.velocity = Vector2(0, self.speed)
        if self.pos.x > RB:
            self.oldPos = self.pos 
            self.pos = Vector2(RB - 2, self.pos.y)
            self.velocity = Vector2(0, self.speed)
        if self.pos.y > self.oldPos.y + yStep:
            if self.pos.x < 300:
                self.velocity = Vector2(self.speed, 0)
            else: self.velocity = Vector2(-self.speed, 0)
            self.oldPos = self.pos


class Jellies(GameObject): #AKA powerups
    def __init__(self, position):
        self._size = 0.1
        self._position = position
        self._properties = 0

        # determines what property the jelly will have
        if bernoulli(0.1): self._properties = 3
        elif bernoulli(0.2): self._properties = 2
        elif bernoulli(0.5): self._properties = 1
        elif bernoulli(0.5): self._properties = 0
        elif bernoulli(0.3): self._properties = 'h'
        elif bernoulli(0.2): self._properties = 'b'

        jelly = rotozoom(load_sprite(f"jelly_{self._properties}"), 0, self._size)
        self.hitbox = jelly.get_height() / 6
        super().__init__(self._position, jelly, Vector2(0, 1)*JELLY_SPEED)

    # determines if a jelly will drop
    def Spawn():
        return bernoulli(0.2)

    # returns the type of jelly that dropped
    def Collect(self):
        return self._properties            