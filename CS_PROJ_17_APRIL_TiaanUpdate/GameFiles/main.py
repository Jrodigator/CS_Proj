# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                                                       # #
#                                                                                                                                       #  #
#    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    #   #
#    #  $$\   $$\ $$$$$$\ $$\    $$\ $$$$$$$$\  #  $$$$$$\ $$\   $$\ $$\    $$\  $$$$$$\  $$$$$$$\  $$$$$$$$\ $$$$$$$\   $$$$$$\   #    #    #
#    #  $$ |  $$ |\_$$  _|$$ |   $$ |$$  _____| #  \_$$  _|$$$\  $$ |$$ |   $$ |$$  __$$\ $$  __$$\ $$  _____|$$  __$$\ $$  __$$\  #    #     #
#    #  $$ |  $$ |  $$ |  $$ |   $$ |$$ |       #    $$ |  $$$$\ $$ |$$ |   $$ |$$ /  $$ |$$ |  $$ |$$ |      $$ |  $$ |$$ /  \__| #    #     #
#    #  $$$$$$$$ |  $$ |  \$$\  $$  |$$$$$\     #    $$ |  $$ $$\$$ |\$$\  $$  |$$$$$$$$ |$$ |  $$ |$$$$$\    $$$$$$$  |\$$$$$$\   #    #     #
#    #  $$  __$$ |  $$ |   \$$\$$  / $$  __|    #    $$ |  $$ \$$$$ | \$$\$$  / $$  __$$ |$$ |  $$ |$$  __|   $$  __$$<  \____$$\  #    #     #
#    #  $$ |  $$ |  $$ |    \$$$  /  $$ |       #    $$ |  $$ |\$$$ |  \$$$  /  $$ |  $$ |$$ |  $$ |$$ |      $$ |  $$ |$$\   $$ | #    #     #
#    #  $$ |  $$ |$$$$$$\    \$  /   $$$$$$$$\  #  $$$$$$\ $$ | \$$ |   \$  /   $$ |  $$ |$$$$$$$  |$$$$$$$$\ $$ |  $$ |\$$$$$$  | #    #     #
#    #  \__|  \__|\______|    \_/    \________| #  \______|\__|  \__|    \_/    \__|  \__|\_______/ \________|\__|  \__| \______/  #    #     #
#    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    #     #
#                                                                                                                                       #     #
#                    .' '.            __       # # # # # # # # # # # # # # # #          __         .' '.                                #     #
#           .        .   .           (__\_     #  JARED RODRIGUES 25983792   #        _/__)        .   .       .                        #     #
#            .         .         . -{{_(|8)    #  ROSS                       #       (8|)_}}- .      .        .                         #     #
#              ' .  . ' ' .  . '     (__/      #  TIAAN Mouton 26017377      #        `\__)    '. . ' ' .  . '                          #    #
#                                              # # # # # # # # # # # # # # # #                                                          #   #
#                                                                                                                                       #  #
#                                                                                                                                       # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

## FEATURES 
## NO ChatGPT 
## Custom Sprites and Backgrounds
## Sounds from free online sound effect libraries from Mixkit.co


import menu, game, pygame

if __name__ == "__main__":
    
    while True:
        pygame.init()
        #bg_music = pygame.mixer.Sound("Assets\The Only Thing They Fear Is You.wav")
        #bg_music.play(loops = -1)  
        instance = menu.Title_Screen()
        instance.title_loop()  


## STRAIGHT TO GAME

# if __name__ == "__main__":       
    # #instance = Menu()
    # instance = Game(2)
    # instance.game_loop()  
    

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