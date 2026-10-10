import pygame as pg
import os
import random
from constants import Constants
from player import Player


c = Constants
screen = c.screen
W = c.WIDTH
H = c.HEIGHT
W2 = c.W2
H2 = c.H2
QW = W / 4
HW = W/2
HH = H /2
QH = H / 4


class Expanding_Galaxy:
    def __init__(self, player):
        self.colorlist=[pg.Color(self.color) for self.color in [
           "white", "gray59", "turquoise1", "mediumspringgreen", 
            "lavender", "cyan1", "cyan2", "aquamarine", "aquamarine2",
            "antiquewhite", "gray70", "gray80", "maroon", "khaki",
            "darkturquoise", "cornsilk", "azure1","azure2", "linen", "aliceblue",
            "ivory1", "snow1","snow2", "snow3","paleturquoise1","ivory2",
            "antiquewhite1","antiquewhite2","darkorchid","floralwhite",
            "ghostwhite","gray40","gray50","gray60","gray70","gray80","gray45",
            "gray55","gray65","gray75","gray85","gray25","gray30","gray35","gray42","gray57",
            "gray90","lavenderblush","lightcyan1","lightcyan2","lightcyan3",
            "wheat", "seashell1","seashell2", "seashell3","oldlace","orchid1","paleturquoise1",
            "paleturquoise2","papayawhip","powderblue","purple","rosybrown1","slategray1",
            "slategray2","turquoise1","turquoise2","turquoise3","yellow","whitesmoke","seagreen",
            "lightyellow1","lightyellow2","lightsteelblue","lightblue","lemonchiffon1",
            "lemonchiffon2","honeydew1","honeydew2",
        ]
    ]



        
        self.player = player
        self.cam = self.player.camera
        self.camx, self.camy = self.cam
        self.bgdata = []
        self.player = player
        self.x = 1000
        self.y = 1000
        self.w = W
        self.H = H
       
    # ... (your __init__ and coordinates method remain mostly the same)
    def add_bg(self, camx, camy):
        bg = {}
        color_name = random.choice(self.colorlist)
        radius = 1
        pos = self.coordinates(camx, camy, 3, 3)
        bg["color"] = color_name
        bg["radius"] = radius
        bg["pos"] = pos
        bg["width"] = 3
        bg["height"] = 3
        bg["x"], bg["y"] = pos
        bg["rect"] = pg.Rect((bg["x"], bg["y"], bg["width"], bg["height"]))
        return bg
    def coordinates(self, camx, camy, objw, objh):
      
        self.camxx = 2*self.camx
        self.camyy = 2*self.camy
        self.camrect = pg.Rect(self.camx, self.camy, W, H)
        while 1:
           
            self.startx = int(self.camx) - (W) //1
            self.stopx = int(self.camx) + (W2)// 1
            self.starty = int(self.camy) - (H) //1
            self.stopy = int(self.camy) + (H2)// 1
            self.rx = random.randint(self.startx, self.stopx)
            self.ry = random.randint(self.starty, self.stopy)
            self.objrect = pg.Rect(self.rx, self.ry, objw, objh)
            if not self.objrect.colliderect(self.camrect):
               
                return self.rx, self.ry
    

    def bgupdate(self, camx, camy):
        self.camx, self.camy = camx, camy

        if len(self.bgdata) < 9000:  # reduced the size for performance reasons
            self.bgdata.append(self.add_bg(self.camx, self.camy))

        for bg in self.bgdata:
            mrect = pg.Rect((bg["x"] - self.camx, bg["y"] - self.camy, bg["width"], bg["height"]))

            surf = pg.Surface((6, 6)).convert_alpha()
            pg.draw.circle(surf, bg["color"], (3, 3), bg["radius"])

            screen.blit(surf, mrect.topleft)

        self.bgdata = [bg for bg in self.bgdata if not self.boundaries(self.camx, self.camy, bg)]

    def boundaries(self, camx, camy, bg):
        # Return False if camx and camy are more than
        # a half-window length beyond the edge of the window.
        self.bg = bg
        self.bounds_left = self.camx - W
        self.bounds_top = self.camy - H
        self.boundsrect = pg.Rect(self.bounds_left, self.bounds_top, W2*2, H2*2)
        self.objrect = pg.Rect(self.bg["x"], self.bg["y"], self.bg["width"], self.bg["height"])
        return not self.boundsrect.colliderect(self.objrect)        




    


   
class Galaxy:
    img = pg.image.load('gx/backgrounds/level4.png').convert_alpha()
    rect = img.get_rect()
   
    def __init__(self, player, dt):
        self.player = player
        self.screen = screen.copy()
        self.dt = dt
       
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        
      
        self.sr = screen.get_rect()
       
                 
       
        self.playrect = player.rect
        self.cam = self.player.camera
        self.invcam = self.player.invcam
        self.subcam = self.player.subcam
        self.revcam = self.player.revcam
        self.extcam = self.player.extcam
        self.camx, self.camy = self.cam
        self.playerpos = pg.math.Vector2(player.position)
        self.start = pg.Vector2(1000, 1000)

        self.img2 = self.img.subsurface(self.rect)
        
        
        
        self.img4 = self.img.subsurface(self.rect)
        self.img5 = self.img.subsurface(self.rect)

        
        self.dist = []
        self.dist1 =[i for i in range(1000,100000) if i % 60000 == 0]
        self.dist2=[j for j in range(100000, 1000000) if j % 200000 == 0]
        self.dist3=[k for k in range(1000000, 100000000) if k % 300000 == 0]
        self.distance, self.projected, self.projected2 = player.update(dt)
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x, self.y = self.playerpos
                    

   


    def draw(self, surface, dt):
        self.dt = dt

        self.distance, self.projected, self.projected2 = self.player.update(dt)
       
        surface.blit(self.img, -self.cam)
        
    def update(self, dt):

        self.distance, self.projected, self.projected2 = self.player.update(dt)
      
    
        self.blitdistance = self.distance * 2
        for distance in self.dist2:
            if self.blitdistance > distance:
                planet1 = pg.image.load("gx/planets/P47.png").convert_alpha()
                screen.blit(planet1,  self.extcam, self.rect2)
                screen.blit(self.img4, self.revcam, self.rect)
                screen.blit(self.img5, self.revcam, self.rect)
                screen.blit
                for blitdistance in self.dist2:
                    if self.blitdistance > distance:
                     
                        screen.blit(self.img2, self.extcam, self.rect4)
                        screen.blit(self.img5, self.extcam, self.rect5)
                        screen.blit(self.img4, self.extcam, self.rect)
                for distance in self.dist3:
                    if self.blitdistance > distance:
                       
                        screen.blit(self.img11,  self.extcam, self.rect11) 
                    

class Stars:
    def __init__(self, player):
        
       
        self.player = player
        self.cam = self.player.camera
        self.sizex = int(1300)
        self.sizey = int(800)
        self.size = (1300, 800)
        self.invcam = self.player.invcam
        self.subcam = self.player.subcam
        self.revcam = self.player.revcam
        self.extcam = self.player.extcam
        self.camx, self.camy = self.cam
        self.center_pos = (650, 400)
        self.bg = pg.Surface((self.size))
        self.rect = self.bg.get_rect()
        self.bg.set_colorkey((0, 0, 0))
        self.color = [0,0,0,0]
       
              

       
      
        
    def starmap(self):
        
     
        wht = pg.Color('white')
        gry = pg.Color('gray59')
        gry2 = pg.Color('gray80')
        gry3 = pg.Color('gray93')
        snow = pg.Color('snow')
        ivory = pg.Color('ivory')
        cyan = pg.Color("turquoise1")
        colorlist = [wht, gry, gry2, gry3, snow, ivory, cyan]
       
        for self.color in colorlist:
            
            for self.stars in range(10):
                self.color = random.choice(colorlist)
                self.starx = random.randint(10, self.sizex)
                self.stary = random.randint(10, self.sizey)
                self.star = self.starx, self.stary
                self.radius = 1
                for self.stars in range(5):
                    self.color = random.choice(colorlist)
                    self.starx = random.randint(10, self.sizex)
                    self.stary = random.randint(10, self.sizey)
                    self.star = self.starx, self.stary
                    self.radius = 1
                    pg.draw.circle(self.bg, self.color, self.star, self.radius)


     



