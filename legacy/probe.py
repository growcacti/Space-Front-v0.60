import pygame as pg
import math
from math import tan, copysign
from math import pi, hypot, cos, sin, atan2, degrees, radians
from pygame.math import Vector2
from constants import Constants

con = Constants










class Probe:
    def __init__(self, pos, direction, player):

        self.player = player
     
        self.cam = player.camera
    
        self.x, self.y = pos
        self.pos = self.x, self.y
        self.dir = Vector2(direction)
        self.counter = 0
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (-1, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
            angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.probe = pg.image.load('gx/ships/probe.png').convert_alpha()
        self.probe_rect = pg.Rect(self.probe.get_rect(center = self.pos -self.cam))
      
        self.probe = pg.transform.rotate(self.probe, angle)
        self.probe_rect.move_ip(-1,0)
        self.speed = 0.2
        self.update()
        
    def update(self):
        
        self.pos = (self.pos[0]-self.dir[0]*self.speed, 
                    self.pos[1]-self.dir[1]*self.speed)
    def move_away_from_player(self):
        
        self.dir = self.pos - self.player.position  # Reversing the subtraction here
        if self.dir.length_squared() > 0:
            self.dir.normalize_ip()
          
        self.vel += self.dir * 0.02

        # Update last_direction based on movement direction
        if abs(self.dir.x) > abs(self.dir.y):
            if self.dir.x > 0:
                self.last_direction = (1,0)
            else:
                self.last_direction = (-1,0)
        elif abs(self.dir.x) < abs(self.dir.y):
            if self.dir.y > 0:
                self.last_direction = (0,1)
            else:
                self.last_direction = (0,-1)


    def draw(self, surf):
        if self.counter == 0:
            probe_rect = self.probe.get_rect(center = self.pos - self.cam)
           
            surf.blit(self.probe, probe_rect)
            self.counter = 0
        else:
            self.counter = 0

        pg.display.flip()               
