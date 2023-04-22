# pygame imports
import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame.mouse import get_pos as gp 
# header file imports
from utils import load_sprite, load_sound
# python imports
import math
import random as r 
from stdrandom import bernoulli

BULLETSPEED = 8
PROJECTILESPEED = 6
ENEMY_SPEED = 2.8
BEE_SPEED = 1.8
JELLY_SPEED = 2


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
        draw_position = self.pos - Vector2(self.sprite.get_width() / 2) # Vector2(self.hitbox)
        # draw from center position 
        screen.blit(self.sprite, draw_position)

        
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

# Bee class (player) -> has a speed, can shoot (bullets), can move (left, right)

class Bee(GameObject):
    def __init__(self, position):

        
        self.shoot_sound = load_sound("shoot")
        self.direction = Vector2(UP)
        sprite = load_sprite("Bee")
        super().__init__(position, sprite, Vector2(0))
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

# Stinger Class (player) -> acts as the gun/ turret

class Stinger(GameObject):
    def __init__(self, position):
        self.direction = Vector2(UP)
        sprite = load_sprite("stinger")
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

# Barrier Class -> has 4 hitpoints, slowly breaks down     

class Barrier(GameObject):
    def __init__(self, position, size=0.7):
        self.level = [rotozoom(load_sprite(f"Barrier{i}"), 0, size)for i in range(5)]
        self.size = size
        self.hitbox = load_sprite("Barrier0").get_width() / 4
        barrier = self.level[0]

        super().__init__(position, barrier, Vector2(0), Hp = 4)
    
    def update_damage(self):
        p = r.randint(0, 1) # 50% chance of taking damage
        if p == 1:
            self.hitPoints -= 1
            self.sprite = self.level[4 - self.hitPoints]

# Bullets Class (player) -> has a speed

class Bullets(GameObject):
    
    def __init__(self, position, velocity, angle, size=0.1, type = 0):
        self.size = size

        # load sprite
        if (type == 0): 
            sprite = load_sprite("bull00")
            self.damage = 0.5
            scale = 0.8
        elif (type == 1): 
            sprite = load_sprite("bull01")
            self.damage = 1
            scale = 0.8
        elif (type == 2): 
            sprite = load_sprite("bull02")
            self.damage = 1.5
            scale = 0.5
        # rotate sprite to direction of Bee
        rotatedSprite = rotozoom(sprite, -angle, scale)
        
        super().__init__(position, rotatedSprite, velocity*BULLETSPEED)

        self.hitbox = sprite.get_height() / 6
        self.image = sprite
        self.rect = self.image.get_rect(center = position) #topleft = (position.x,position.y)

# Projectiles class (enemies) -> has a type that affects its sprite, damage and speed

class Projectile(GameObject):
    def __init__(self,  position, velocity, angle = 0, type = 0, size=0.1):
        self.size = size * (type + 1)

        sprite = load_sprite(f"projectile{type}")
        rotatedSprite = rotozoom(sprite, -angle, 1)
        self.hitbox = sprite.get_height() / 6

        super().__init__(position, rotatedSprite, velocity*PROJECTILESPEED)

# Lives Class -> has a size that affects its sprite

class Lives(GameObject):
    def __init__(self, position, size=0.4):
        self.size = size
        life = rotozoom(load_sprite("Life"), 0, size)

        super().__init__(position, life, Vector2(0))

# Enemies class -> has a type that affects its sprite, lives and damage
    # 1 - Ant -> 1 Dmg, 1 Hp 
    # 2 - Bird -> 2 Dmg, 3 Hp
    # 3 - Bear -> InstaKill, 10 Hp (Boss Battle)

class Enemy(pygame.sprite.Sprite): # from alien
    def __init__(self,type,x,y):
        super().__init__()
        file_path = f'assets/enemy{type}.png'
        self.image = rotozoom(pygame.image.load(file_path).convert_alpha(), 0, 0.5)
        self.rect = self.image.get_rect(topleft = (x,y))
        self.pos = self.rect.center
        self.type = type
        
        if type == 0: 
            self.hitpoints = 1
            self.image = pygame.transform.rotate(self.image, 180)
            self.hitbox = load_sprite("Ant").get_width() / 3
        elif type == 1: 
            self.hitpoints = 3
            self.hitbox = load_sprite("Bird").get_width() / 3
        else: 
            self.hitpoints = 50
            # self.image = rotozoom(pygame.image.load(file_path).convert_alpha(), 0, 2)
            self.hitbox = load_sprite("Bear").get_height() / 2
            self.image = rotozoom(pygame.image.load(file_path).convert_alpha(), 0, 2)
            self.rect = self.image.get_rect(topleft = (x,y))
            self.pos = self.rect.center

    def collider(self, entity):
        distance = self.pos.distance_to(entity.pos)
        return distance < self.hitbox + entity.hitbox
    
    def update(self,direction):
        self.rect.x += direction
        self.pos = self.rect.center


class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width):
        super().__init__()
        self.image = rotozoom(pygame.image.load('assets/Bird.png').convert_alpha(), 0, 0.5)
		
        if side == 'right':
            x = screen_width + 50
            self.speed = - 3
        else:
            x = -50 
            self.speed = 3

        self.hitpoints = 3
        self.hitbox = load_sprite("bird").get_width() / 3
        self.rect = self.image.get_rect(topleft = (x,80))
        self.pos = self.rect.center

    def update(self):
        self.rect.x += self.speed
        self.pos = self.rect.center

# Jellies class -> has a property that affects the Bee
class Jellies(GameObject): # AKA powerups
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
