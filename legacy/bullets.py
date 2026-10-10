import pygame as pg
import math
from math import tan, copysign
from math import pi, hypot, cos, sin, atan2, degrees, radians
from pygame.math import Vector2
from constants import Constants
con = Constants
screen = con.screen
class Bullet:
    def __init__(self, pos, direction):
        self.x, self.y = pos
        self.pos = self.x, self.y

        self.dir = direction
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
            self.angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.image = pg.Surface((9, 9)).convert_alpha()
        self.image.fill((255,128,0))
        self.image.set_colorkey((0, 0, 0, 0))
        pg.draw.circle(self.image, pg.Color("red"), (4, 3), 3)
        pg.draw.circle(self.image, pg.Color("purple"), (1, 1), 2)
        pg.draw.circle(self.image, pg.Color("yellow"), (4, 4), 3)

        self.image = pg.transform.rotate(self.image, angle)
        self.speed = 5
       
    def update(self):
        
        self.pos = (self.pos[0]+self.dir[0]*self.speed, self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        self.rect = self.image.get_rect(center = self.pos)
        self.rect3 = pg.Rect(self.image.get_rect(center=self.pos))
        self.hitbox = pg.draw.rect(screen, (255,0,0), self.rect3,3)

        screen.blit(self.image, self.rect)
        surf.blit(self.image, self.rect)
        
        
class Projectile:
    def __init__(self, pos, direction):
        self.x, self.y = pos
        self.pos = self.x, self.y
    
        self.dir = direction
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
            self.angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.image = pg.Surface((13, 13)).convert_alpha()
        self.image.fill((0,0,255))
        self.image.set_colorkey((0, 0, 0, 0))
        pg.draw.circle(self.image, pg.Color("cyan"), (3, 4), 5)
        pg.draw.circle(self.image, pg.Color("green"), (3, 4), 5)

        self.image = pg.transform.rotate(self.image, angle)
        self.speed = 5
        self.update()
    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        self.rect = self.image.get_rect(center = self.pos)
        self.rect3 = pg.Rect(self.image.get_rect(center=self.pos))
        self.hitbox = pg.draw.rect(screen, (0,255,0), self.rect3,3)

        screen.blit(self.image, self.rect)
        surf.blit(self.image, self.rect)
        
class Photon:
    def __init__(self, pos, direction, images):
        self.x, self.y = pos
        self.pos = self.x, self.y
        self.images = images
        self.image = self.images[0]
        self.rect=pg.Rect(self.image.get_rect(center=self.pos))
        self.current_frame = 0
        self.frame_duration = 5  # Adjust this for faster or slower animation
        self.frame_timer = 0

        self.dir = direction
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
            self.angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.image = self.images[self.current_frame]
        self.speed = 0.8

    def update(self):
        self.pos = (
            self.pos[0] + self.dir[0] * self.speed,
            self.pos[1] + self.dir[1] * self.speed,
        )

        # Update animation
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.frame_timer = 0

    def draw(self, surf):
        rect = self.image.get_rect(center=self.pos)
        hitbox = pg.draw.rect(screen, (255, 0, 0), rect, 3)

        screen.blit(self.image, rect)
        surf.blit(self.image, rect)


