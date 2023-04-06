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

def print_text(surface, text = "", font = 32, colour = (255, 0, 0)):
    font = Font('freesansbold.ttf', font)
    text = font.render(text, True, colour)
    rect = text.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text, rect)