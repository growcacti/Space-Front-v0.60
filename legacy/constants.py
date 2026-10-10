import pygame as pg




class Constants:
   
   
    WIDTH = 1300
    HEIGHT = 800
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.HWSURFACE | pg.RESIZABLE)
    screen_rect = screen.get_rect(center = screen.get_rect().center)
    displaysurf = screen.copy()
    SIZE = (WIDTH, HEIGHT)
    W = WIDTH
    H = HEIGHT
    W2 = 2*W
    H2 = 2*H
    HW = W / 2
    QW = W / 4
    HQW = HW + QW
    HH = H /2
    QH = H / 4
    HQH = HH + QH
    clock = pg.time.Clock()
    ticks = 30
    fps = ticks
    dt = fps / 1000
    WHITE = ((255,255,255))
    ORANGE = ((255,165,0))
    BLUE = ((0,0,255))
    GREEN = ((0,255,0))
    CYAN = ((0,255,255))
    YELLOW = ((255,255,0))
    RED= ((255,0,0))
    


