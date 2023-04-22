from pygame.font import Font 
from pygame.image import load
from pygame.mixer import Sound
from pygame.math import Vector2

def load_sprite(name):
    path = f"assets/{name}.png"
    sprite = load(path)

    return sprite

def load_sound(name):
    path = f"assets/{name}.wav"
    return Sound(path)

def print_text(surface, text = "", font = 32, colour = (0, 0, 0)):
    font = Font('freesansbold.ttf', font)
    text1 = font.render(text, True, colour)
    text2 = font.render(text, True, (200, 30, 30))
    rect = text1.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text1, rect)
    rect.center = Vector2(surface.get_size()) / 2 + (2, 2)
    surface.blit(text2, rect)

# sort file method 
def sort_score():
    path = f"scores.txt"

def update_score():
    x = 1

def check_if_high_enough(score):
    pass