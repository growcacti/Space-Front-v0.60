import pygame as pg
import sys
import os
from player import Player
from constants import Constants


c = Constants
screen =c.screen

class Controls:
    def __init__(self, player,dt):
        self.button = pg.Rect(10, 10, 30, 30)
        self.button2 = pg.Rect(30, 75, 30, 30)
        self.button3 = pg.Rect(50, 125, 30, 30)
        self.button4 = pg.Rect(80, 175, 30, 30)
##        self.button5 = pg.Rect(50, 10, 5, 5)
##        self.button6 = pg.Rect(50, 25, 5, 5)
##        self.button7 = pg.Rect(50, 40, 5, 5)
##        self.button8 = pg.Rect(50, 60, 5, 5)
##        self.button9 = pg.Rect(100, 10, 5, 5)
##        self.button10 = pg.Rect(100, 25, 5, 5)
##        self.button11 = pg.Rect(100, 40, 5, 5)
##        self.button12 = pg.Rect(100, 60, 5, 5)
##        self.button13 = pg.Rect(100, 25, 5, 5)
##        self.button14 = pg.Rect(150, 10, 5, 5)
##        self.button15 = pg.Rect(150, 25, 5, 5)
##        self.button16 = pg.Rect(150, 40, 5, 5)
##        self.button17 = pg.Rect(150, 60, 5, 5)
##        self.button18 = pg.Rect(200, 10, 5, 5)
##        self.button19 = pg.Rect(200, 25, 5, 5)
##        self.button20 = pg.Rect(200, 40, 5, 5)
##        self.button21 = pg.Rect(200, 60, 5, 5)
##        self.button22 =pg.Rect(650, 10, 25, 25)
##        self.button23 = pg.Rect(350, 10, 35, 35)
        self.player = player
        self.dt = dt
       



    def buttons(self, dt):
        self.dt = dt
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_rel = pg.mouse.get_rel()
       

        if self.button.collidepoint(self.mouse_pos):
         
            self.warp = 0
            self.player.update(self.dt, self.warp)
          
         

        if self.button2.collidepoint(self.mouse_pos):
           
            self.warp = 1
            self.player.update(self.dt, self.warp)
          

        if self.button3.collidepoint(self.mouse_pos):
           
            self.warp = 2
            self.player.update(self.dt, self.warp)

        if self.button4.collidepoint(self.mouse_pos):
            self.warp = 3
            self.player.update(self.dt, self.warp)

                 
##                     if self.button5.collidepoint(self.mouse_pos):
##                         st.grid(5) 
##                         
##                                          
##                     if self.button6.collidepoint(self.mouse_pos):
##                         st.grid(6)
##                     if self.button7.collidepoint(self.mouse_pos):
##                         st.grid(7)
##                    
##                       
##                     if self.button8.collidepoint(self.mouse_pos):
##                        st.grid(8)
##                     if self.button9.collidepoint(self.mouse_pos):
##                        st.grid(9)
##                     if self.button10.collidepoint(self.mouse_pos):
##                        pass                         
##                     if self.button11.collidepoint(self.mouse_pos):
##                         pass
##                      
##                 
##                             
##                         
##                     if self.button12.collidepoint(self.mouse_pos):
##                         pass
##                         
##                     if self.button13.collidepoint(self.mouse_pos):
##                         pass
##                         
##                     if self.button14.collidepoint(self.mouse_pos):
##                         pass
##                         
##
##
##                     if self.button15.collidepoint(self.mouse_pos):
##                         st.grid(10)
##                         
##                     if self.button16.collidepoint(self.mouse_pos):
##                         st.grid(11)
##                         
##                     if self.button17.collidepoint(self.mouse_pos):
##                         st.grid(12)
##
##                     if self.button18.collidepoint(self.mouse_pos):
##                         st.grid(13) 
##                        
##                                          
##                     if self.button19.collidepoint(self.mouse_pos):
##                         st.grid(14)
##                         
##                     if self.button20.collidepoint(self.mouse_pos):
##                    
##                         print('self.button20 was pressed at {0}'.format(self.mouse_pos))
##
##                     if self.button21.collidepoint(self.mouse_pos):
##                        # prints current location of mouse
##                         print('self.button21 was pressed at {0}'.format(self.mouse_pos))
##                     if self.button22.collidepoint(self.mouse_pos):
##                        # prints current location of mouse
##                         print('self.button22 was pressed at {0}'.format(self.mouse_pos))
##                     if self.button23.collidepoint(self.mouse_pos):
##                         st.grid(23)
##                             
##                   



                 
##            # extra experimental features       
##            if pressed[pg.K_r]:
##                st.grid(1)
##            if pressed[pg.K_g]:
##                st.grid(2)
##                
##            if pressed[pg.K_F11]:
##                st.grid(3)
##            if pressed[pg.K_F12]:
##                st.grid(4)
##                                    
##            if pressed[pg.K_o]:
##                st.grid(5)              
##                            

    def create_buttons(self):

        pg.draw.rect(screen, pg.Color(200, 0, 0, 100), self.button)
        pg.draw.rect(screen, pg.Color(200,125,0,100), self.button2)
        pg.draw.rect(screen, pg.Color(200,200,0,110), self.button3)
        pg.draw.rect(screen, pg.Color(0, 0, 200,100), self.button4)
##        pg.draw.rect(screen, pg.Color(0, 200,0,110), self.button5)
##        pg.draw.rect(screen, pg.Color(0, 200,0,100), self.button6)
##        pg.draw.rect(screen, pg.Color(0, 200, 0, 110), self.button7)
##        pg.draw.rect(screen, pg.Color(0, 200, 0, 110), self.button8)
##        pg.draw.rect(screen, pg.Color(59, 59, 59, 110), self.button9)
##        pg.draw.rect(screen, pg.Color(58, 58, 58, 110), self.button10)
##        pg.draw.rect(screen, pg.Color(57, 57, 57, 110), self.button11)
##        pg.draw.rect(screen, pg.Color(81,81,81,110), self.button12)
##        pg.draw.rect(screen, pg.Color(255,255,60,110), self.button13)
##        pg.draw.rect(screen, pg.Color(10, 250, 250,110), self.button14)
##        pg.draw.rect(screen, pg.Color(250, 100, 255, 110), self.button15)
##        pg.draw.rect(screen, pg.Color(145,120,127, 110), self.button16)
##        pg.draw.rect(screen, pg.Color(140,140,140, 110), self.button17)
##        pg.draw.rect(screen, pg.Color(255, 255, 0, 110), self.button18)
##        pg.draw.rect(screen, pg.Color(220,200,0,140), self.button19)
##        pg.draw.rect(screen, pg.Color(0, 255, 255,140 ), self.button20)
##        pg.draw.rect(screen, pg.Color(255, 100, 255, 140), self.button21)
##        pg.draw.rect(screen, pg.Color(216, 191, 216, 145), self.button22)
##        pg.draw.rect(screen, pg.Color(255, 255, 255, 100), self.button23)
##
##
##
