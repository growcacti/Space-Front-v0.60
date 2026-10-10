import pygame as pg
import math
from math import tan, copysign
from math import pi, hypot, cos, sin, atan2, degrees, radians
from pygame.math import Vector2
from constants import Constants
import get_info




c = Constants
screen = c.screen
WIDTH = c.WIDTH
HEIGHT = c.HEIGHT
W = c.W
H = c.H
CW = W // 2
CH = H // 2
W2 = W * 2
H2 = H * 2
class Player:
    def __init__(
        self, image, x=CW, y=CH, angle=0.0, length=4, max_rotation=10, max_acceleration=5.0):
        self.orig_image = image
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = self.image.get_size()
        self.rect = pg.Rect(self.image.get_rect(center=(x, y)))
        #self.rect = self.image.get_rect(center=(x, y))
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = 4
        self.max_rotation = max_rotation
        self.max_velocity = 6
        self.thrust = 4
        self.sim_inertia = 0.05  # iner
        self.font = pg.font.Font(None, 20)
        self.acceleration = 0.1
        self.rotation = 0.0
        self.background = Vector2(self.position)
        self.camera = Vector2(0, 0)
        self.cam = self.camera
        self.cam.x, self.cam.y = self.cam
        self.revcam = Vector2(0, 0)
        self.subcam = Vector2(0, 0)
        self.invcam = Vector2(0, 0)
        self.extcam = Vector2(0, 0)
        self.extcam1 = Vector2(1000,1000)
        self.extcam2 = Vector2(5000,5000)
        self.extcam3 = Vector2(10000,10000)
        self.extcam4 = Vector2(50000,50000)
        self.extcam5 = Vector2(2000,2000)
        self.extcam6 = Vector2(100,100)
        self.fcam = Vector2(0, 0)
        # Assigned the camera.era as an attribute.
        self.direction = Vector2(0, 0)
        self.warp = 0
        self.camrect = pg.Rect(self.cam.x,self.cam.y,W,H)
        self.fuel = 900000
        self.shields = 100
        self.hitcount = 0
       
    def update(self, dt, warp=0):
        self.warp = warp
        if self.warp == 0:
            self.max_velocity = 2
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
            self.velocity.y = max(-self.max_velocity, min(self.velocity.y, self.max_velocity))
            self.velocity += (self.acceleration * dt, 0)
            self.fuel -= 1                    
        elif self.warp == 1:
            self.max_velocity = 12
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
            self.velocity.y = max(-self.max_velocity, min(self.velocity.y, self.max_velocity))
            self.velocity += (self.acceleration * 2 * dt, 0)
            self.fuel -= 1          
        elif self.warp == 2:
            self.max_velocity = 18
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
            self.velocity.y = max(-self.max_velocity, min(self.velocity.y, self.max_velocity))
            self.velocity += (self.acceleration, 0)
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
            if self.rotation:
                turning_radius = self.length / tan(radians(self.rotation))
                angular_velocity = self.velocity.x / turning_radius / 256
            self.fuel -= 20
        elif self.warp == 3:
            self.max_velocity = 40
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
            self.velocity.y = max(-self.max_velocity, min(self.velocity.y, self.max_velocity))
            self.velocity += (self.acceleration, 0)
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
            if self.rotation:
                turning_radius = self.length / tan(radians(self.rotation))
                angular_velocity = self.velocity.x / turning_radius / 1024

            self.fuel -= 100
        else:
            self.max_velocity = 80
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
            self.velocity.y = max(-self.max_velocity, min(self.velocity.y, self.max_velocity))
            self.velocity += (self.acceleration * dt, 0)
      

        if self.rotation:
            turning_radius = self.length / tan(radians(self.rotation))
            angular_velocity = self.velocity.x / turning_radius / 8
        else:
            angular_velocity = 0

        vel = self.velocity.rotate(-self.angle) * dt
        self.position += vel
        fvel = vel * 1.1
        bvel = vel / -300
        
        cvel = vel / -10
        rvel = vel / -1
        svel = vel / -40
        invvel = vel / -100
        extvel = vel / -400
        self.camera += cvel  # Update the camera.era position as well.
        self.revcam += rvel
        self.subcam += svel
        self.invcam += invvel
        self.extcam += extvel
        self.extcam1 += svel
        self.extcam2 += svel
        self.extcam3 += svel
        self.extcam4 += svel
        self.extcam5 += svel
        self.extcam6 += svel
        self.background += bvel
        self.fcam -= fvel
        # If you use the rect as the blit position, you should update it, too.
        self.rect.center = self.position
        self.angle += degrees(angular_velocity) * dt
       
        self.image = pg.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect2 = self.image.get_rect()
        self.rect3 = pg.Rect(self.image.get_rect(center=self.rect.center-self.camera))
        self.hitbox = pg.draw.rect(screen, (255,0,0), self.rect3,3)

        #self.direction = self.angle
        self.direction = pg.Vector2(1, 0).rotate(-self.angle)
        pg.display.set_caption("Space Fronteerer")
 
        text1 = self.font.render("position: " + str(self.position), True, c.WHITE)
       
        c.screen.blit(text1, (c.WIDTH - 200, c.HEIGHT - 750))
    
        origin = (650, 400)
        destination = self.rect.center
        svp = math.sqrt (vel[0] ** 2 + vel[1]**2) * 671000000
        sp = abs(svp) // 100000
        
        distance, angle, x_ref, y_ref, op_ang, project, project2 =  get_info.info(origin, destination)
        dist = distance // 1
        show_angle = self.angle % 360
                
        self.project = project[0] // 1, project[1] // 1
        self.project2 = project2[0] // 1, project2[1] // 1
        text2 = self.font.render("Distance from Start: " + str(dist), True, c.WHITE)
        c.screen.blit(text2, (c.WIDTH - 200, c.HEIGHT - 780))
        text3 = self.font.render("Angle " + str(show_angle), True, c.WHITE)
        c.screen.blit(text3, (c.WIDTH - 200, c.HEIGHT - 770))
        text5 = self.font.render("MPH " + str(sp), True, c.WHITE)
        c.screen.blit(text5, (c.WIDTH - 200, c.HEIGHT - 760))
    
        self.projected = int(self.project[0]), int(self.project[1])
       
        self.projected2 = int(self.project2[0]), int(self.project2[1])
        self.distance = distance
        text6 = self.font.render("projected1 " + str(self.projected), True, c.WHITE)
        c.screen.blit(text6, (c.WIDTH - 200, c.HEIGHT - 720))


        text7 = self.font.render("Sheilds " + str(self.shields), True, c.WHITE)
        screen.blit(text7, (c.WIDTH - 200, c.HEIGHT - 680))
        
        text8 = self.font.render("Fuel " + str(self.fuel), True, c.WHITE)
        screen.blit(text8, (c.WIDTH - 200, c.HEIGHT - 700))
        
        
        text9 = self.font.render("hits" + str(self.hitcount), True, c.WHITE)
                    
        screen.blit(text9, (c.WIDTH - 200, c.HEIGHT - 800))
            

        return self.distance, self.projected, self.projected2
    def offset(self):
        MARGINX = 550
        MARGINY = 350
        self.cam = self.camera 
     
        
        if (self.cam.x + CW) - self.position.x > MARGINX:
        
            self.cam.x = (self.position.x + MARGINX - CW) 

        elif self.position.x - (self.cam.x + CW) > MARGINX:
            self.cam.x = (self.position.x - MARGINX - CW) 
        if (self.cam.y + CH) - self.position.y > MARGINY:
            self.cam.y = int(self.position.y + MARGINY - CH) 
        elif self.position.y - (self.cam.y + CH) > MARGINY:
            self.cam.y = int(self.position.y - MARGINY - CH)

    def offset2(self):
        mx = 400
        my = 200
        self.cam = self.camera 
     
        
        if (self.cam.x + CW) - self.position.x > mx:
        
            self.cam.x = (self.position.x + mx - CW) 

        elif self.position.x - (self.cam.x + CW) > mx:
            self.cam.x = (self.position.x - mx - CW) 
        if (self.cam.y + CH) - self.position.y > my:
            self.cam.y = int(self.position.y + my - CH) 
        elif self.position.y - (self.cam.y + CH) > my:
            self.cam.y = int(self.position.y - my - CH)

      
    def surface_offset(self):
        self.extx, self.exty = self.extcam
        self.extnegx, self.extnegy = -self.extcam
        self.extposx = 2 * self.position.x
        self.extposy = 2 * self.position.y

class Thruster():
    def __init__(self,ppthrust, direction,ang,thr_img):
        
        self.x = ppthrust[0]
        self.y = ppthrust[1]
        self.pos = self.x, self.y
        self.images = thr_img
        self.current_frame = 0
        self.frame_duration = 2  # Adjust this for faster or slower animation
        self.frame_timer = 0

        self.dir = direction
        self.angle = ang
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
            self.angle = math.degrees(math.atan2(self.dir[0], -self.dir[1]))

        self.image = self.images[self.current_frame]
        self.image = pg.transform.rotate(self.image,-self.angle)  

    def update(self,ang):
        self.angle = ang
        self.pos = (
            self.pos[0] - self.dir[0],
            self.pos[1] - self.dir[1],
        )

        # Update animation
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.frame_timer = 0
            self.image = pg.transform.rotate(self.image, -self.angle)
    def draw(self, surf):
        self.image = pg.transform.rotate(self.image, -self.angle)
        
        rect = self.image.get_rect(center=self.pos)
        
        #hitbox = pg.draw.rect(screen, (255, 0, 0), rect, 3)

        screen.blit(self.image, rect)
        surf.blit(self.image, rect)



