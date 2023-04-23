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
#              ' .  . ' ' .  . '     (__/      #  TIAAN                      #        `\__)    '. . ' ' .  . '                          #    #
#                                              # # # # # # # # # # # # # # # #                                                          #   #
#                                                                                                                                       #  #
#                                                                                                                                       # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import menu, game, pygame, highscore

start = "Menu" # "Menu" or "Game" or "leaderboard"

# MENU LOOP

if __name__ == "__main__" and start == "Menu":  
    while True:  
        instance = menu.Title_Screen()
        instance.title_loop()  
        
## STRAIGHT TO GAME

if __name__ == "__main__" and start == "Game":       
  instance = game.Game(6)
  instance.game_loop()

## STRAIGHT TO LEADERBOARD
    
if __name__ == "__main__" and start == "leaderboard":       
  instance = highscore.HighScore(500)
  instance.score_loop







## EXTRA 

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