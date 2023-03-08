## JARED RODRIGUES 25983792
## HIVE INVADERS

## ALL CODE WRITTEN BY ME (zero OpenAI)
## sprites all made by me 
## background shader, by me with some equations by @lomateron
## Sounds from free online sound effect libraries from Mixkit.co
## pygame tutorials by RealPython

from game import Game
from menu import Menu

if __name__ == "__main__":
       
    #instance = Menu()
    instance = Menu()
    instance.game_loop()  


## EXTRA 

### ALL SOUNDS Free source from https://mixkit.co/free-sound-effects/

## Sprites made with online pixel art sim 
## Background is a shader made with c++ not yet sure how to make and use wrappers 
## so i simply saved the shader and used it as a sprite 

## SHADER CODE :
## C++ with GLSL :
## 
    # void mainImage( out vec4 fragColor, in vec2 fragCoord )   ==> fragColour is pixel colour for each pixel
    # {
    # 	vec2 u = 10.*fragCoord/iResolution.x;           ==> normalize and scale up screen res
        
    #     vec2 s = vec2(1.,1.732);          ==> Hex angle for Hexagonal coordinates
    #     vec2 a = mod(u     ,s)*2.-s;
    #     vec2 b = mod(u+s*.5,s)*2.-s;      ==> credit to @lomateron for hex coords 
        
    # 	vec4 col = vec4(.5*min(dot(a,a),dot(b,b))) + 0.5;       ==> messes with colours to get yellow hive like
    #     col.x = pow(col.x, 0.5);                              ==> effect that i want

    #     fragColor = col * vec4(0.9, 0.8, 0.2, 0);             ==> switch monochrome to colour and output
    # }