import pygame as pg
import random
import sys
import os
import math
from math import tan, copysign
from math import pi, hypot, cos, sin, atan2, degrees, radians
from pygame.math import Vector2
from galaxy import *
from get_info import *

from player import *
from nme import Nme
from bullets import *
from probe import Probe
from constants import Constants

from controls import Controls
pg.init()

path = os.getcwd()
con = Constants
screen = con.screen
displaysurf = con.displaysurf
screen_rect = con.screen_rect
def main():

        pg.init()
        screen = con.screen
        clock = con.clock
        ticks = con.ticks
        fps = con.fps
        dt = con.dt
       
      
     
        font = pg.font.Font(None, 18)
       
        textsurface = font.render('Screen Grid Options                          greybutton                     off                   green grid            Button5', False, (255, 255, 255))
        displaysurf = pg.Surface((1300,800))
        displayrect = pg.Rect(displaysurf.get_rect())
        ship = pg.image.load("gx/ships/51.png").convert_alpha()
        shtr = pg.image.load("gx/ships/zxx22.png").convert_alpha()
        ship2 = pg.image.load("gx/ships/ship91.png").convert_alpha()
        ship3 = pg.image.load("gx/ships/nmefleet.png").convert_alpha()
        base = pg.image.load("gx/ships/base3.png").convert_alpha()
        player = Player(ship)
          
        bg = Expanding_Galaxy(player)
        st = Stars(player)
        g = Galaxy(player, dt)
      
        control = Controls(player, dt)
       
             
        nme = Nme(ship2, (7000), (5000))
        nme2 = Nme(ship3, (3500), (3200))
        nme2nmedist = Vector2(50, 50)
       
        surf = pg.Surface((3, 3))
        off1 = pg.math.Vector2(-71, -70)
        surf.set_colorkey((0,0,0))
        surf2 = pg.Surface((3, 3))
        surf2.set_colorkey((0,0,0))
       
        screen.set_colorkey((0,0,0))
        projectiles = []
        bullets = []
        photons = []
        thrusters = []
        st.starmap()
        p = Probe(player.position, player.direction, player)
        probes = []
        bullet = Bullet(player.position, player.direction)
        projectile = Projectile(player.position, player.direction)
        hit_count = 0
      
        image_paths = ["pht/pht1.png", "pht/pht2.png","pht/pht3.png", "pht/pht4.png", "pht/pht5.png","pht/pht6.png", "pht/pht7.png", "pht/pht8.png","pht/pht9.png","pht/pht10.png", "pht/pht11.png"]
        images = [pg.image.load(img_path) for img_path in image_paths]         
        photon = Photon(player.position, player.direction,images)     
        photons =[]
        thruster_files =["thr/thr01.png","thr/thr02.png","thr/thr03.png","thr/thr04.png","thr/thr05.png"]
        thr_img = [pg.image.load(thr_path) for thr_path in thruster_files]
       
        counter = 0
        

        time_delay = 500
        timer_event = pg.USEREVENT+1
        pg.time.set_timer(timer_event, time_delay)
         
        loop =1
        while loop:
##            displaysurf.fill((0,0,0,0))
            screen.fill((0,0,0,0))

            g.draw(screen, dt)
            screen.blit(st.bg, st.rect)
           
        
                 
        
            pos = pg.Vector2(player.position)
            ang = player.angle
           
            text8 = font.render("NME position: " + str(nme.position), True, con.WHITE)
       
            screen.blit(text8, (con.WIDTH - 1100, con.HEIGHT - 680))

           
          
        
            v1 = pg.math.Vector2(player.position)
            v2 = pg.math.Vector2(nme.position)
            v3 = pg.math.Vector2(nme2.position)
            off1 = pg.math.Vector2(-61, -60)
            fcam = pg.Vector2(player.fcam)
            pcam = pg.Vector2(player.camera)
            camx, camy = pcam
            pppos = pg.Vector2(player.position - (player.rect.width /2, player.rect.height / 2)- pcam)
            ppbullet = pg.Vector2(player.position - (player.rect.width / 64, player.rect.height / 64)- pcam)
            pthrust = pg.Vector2(player.position - (player.rect.width / 512, player.rect.height / 512)- pcam)
            thoffset = (0, 0)
           
##            nmebullet = pg.Vector2(nme.rect.center - off1)
            nmebullet = pg.Vector2(nme.rect.center - pcam - off1)
            pdir = Vector2(player.direction)
            ndir = nme.direction
            ppthrust = (pthrust - thoffset)

            start_time = pg.time.get_ticks()
            probe_launch = False
            ffppos = pg.Vector2(player.position - (player.rect.width /128, player.rect.height / 128) - player.subcam)
            tppos = pg.Vector2(player.position - (player.rect.width /256, player.rect.height / 256) - pcam)
            control.buttons(dt)
            basepps = (300,300)
            basepos = (basepps - pcam)
            thrust = Thruster(player.rect, pdir,-ang,thr_img)
                                 
            # Event queue
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                        return

                elif event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    return    
                elif event.type == timer_event:
                    counter += 1
                    pdir.normalize()
                    firedir = pdir + ndir
                    projectiles.append(Projectile(nmebullet, firedir))
                    
                    for projectile in projectiles:
                        projectile.draw(con.screen)
                        projectile.rect.inflate(5,5)
                        if projectile.rect3.colliderect(player.rect3):
                            print("majore hit")
                            player.shields -= 1
                            player.hitcount -= 1
                        if player.rect3.colliderect(projectile.rect3):
                            print("majore hit")
                            player.shields -= 1
                            player.hitcount -= 1
                                
                elif event.type == timer_event:
                    if len(projectiles) > 100:
                        projectiles.clear()
                        get_collision_side(player.rect3, nme.rect3) 
                        counter += 1
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        probe_launch = True
                        p.update()
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_p:
                        p.move_away_from_player()
                        probe_launch = True
                        p.update()
                            
                
                    if not probe_launch == False:
                        g.img.blit(p.probe, ffppos)
                    
                       
                       

                if event.type == pg.MOUSEWHEEL:
                    if event.y == 1:
                        player.rotation -= 120 * dt
                    elif event.y == -1:
                        player.rotation += 120 * dt
            
                if event.type == pg.MOUSEMOTION:
                    control.buttons(dt)
   
         
                for projectile in projectiles:
                    projectile.draw(con.screen) 


                      # User input & Controls
            pressed = pg.key.get_pressed()
            pressed2 = pg.mouse.get_pressed(num_buttons=5)
            if pressed[pg.K_UP] or pg.mouse.get_pressed()[0]:
                if player.velocity.x < 0:
                    thrusters.append(Thruster(ppthrust, pdir,ang,thr_img))
                  
                    player.acceleration = player.thrust
                    
                else:
                    player.acceleration  += 890 * dt
                    thrusters.append(Thruster(ppthrust, pdir,ang,thr_img))
                for thrust in thrusters:
                    thrust.draw(screen)                
                    thrust.update(ang)
                    
            elif pressed[pg.K_DOWN] or pg.mouse.get_pressed()[1]:
                if player.velocity.x > 0:
                     
                    player.acceleration = -player.thrust
                    thrusters.append(Thruster(ppthrust, pdir,ang,thr_img))
                else:
                    player.acceleration -= 1 * dt
                    thrusters.append(Thruster(ppthrust, pdir,ang,thr_img))
                for thrst in thrusters:
                    thrust.draw(screen)                
                    thrust.update(ang)
            
               
            elif pressed[pg.K_h]:
                if abs(player.velocity.x) > dt * 10 * player.thrust:
                    player.acceleration = -copysign(
                        player.thrust, player.velocity.x
                    )
                else:
                    player.acceleration = -player.velocity.x / dt
            else:
                if abs(player.velocity.x) > dt * player.sim_inertia:
                    player.acceleration = -copysign(
                        player.sim_inertia, player.velocity.x
                    )
                else:
                    if dt != 0:
                        player.acceleration = -player.velocity.x / dt
                        player.acceleration = max(-player.max_acceleration,
                                                  min(player.acceleration, player.max_acceleration),)


            if pressed[pg.K_RIGHT] or event.type == pg.MOUSEWHEEL:
                player.acceleration = player.thrust
                player.rotation += 20
               
                              
            elif pressed[pg.K_LEFT] or pg.mouse.get_pressed(num_buttons=5)[4]:
                player.acceleration = player.thrust
                player.rotation -= 20
               
               
            else:
                player.rotation = 0
            player.rotation = max(
                -player.max_rotation,
                min(player.rotation, player.max_rotation),
            )

        
            
            if pressed[pg.K_f]:
                if len(projectiles) < 5:   
                    projectiles.append(Projectile(ppbullet, pdir))
                    for projectile in projectiles:
                        projectile.draw(con.screen) 

            for projectile in projectiles[:]:
                projectile.update()
                if not screen.get_rect().collidepoint(projectile.pos):
                    projectiles.remove(projectile)
                           
            for projectile in projectiles:
                projectile.draw(con.screen) 

            if pressed[pg.K_SPACE]:
                if len(photons) < 5:   
                    photons.append(Photon(ppbullet, pdir, images))
                    for photon in photons:
                        photon.draw(con.screen) 

            for photon in photons[:]:
                photon.update()
                if not screen.get_rect().collidepoint(photon.pos):
                    photons.remove(photon)
                           
            for photon in photons:
                photon.draw(con.screen)
                photon.update()

            
                          


            if pg.mouse.get_pressed()[2]:
                if len(bullets) < 10:   
                    bullets.append(Bullet(ppbullet, pdir))
                for bullet in bullets:
                    bullet.draw(con.screen) 

                for bullet in bullets[:]:
                    bullet.update()
                    if bullet.rect.colliderect(nme.rect):
                        print("NME took a hit!")
                    if bullet.rect.colliderect(nme2.rect):
                        print("NME2 took a hit!")
                    if not screen.get_rect().collidepoint(bullet.pos):
                        bullets.remove(bullet)

                for bullet in bullets:
                     bullet.draw(con.screen) 
            if len(thrusters) > 20:
                thrusters.clear()         
##            elif player.max_velocity > 110 & len(thrusters) > 30:
##                thrusters.clear()                          
##                                   
##        
##            elif player.max_velocity > 1000 & len(thrusters) > 45:
##                thrusters.clear()
##
##       
##    
##            elif player.max_velocity > 18000 & len(thrusters) > 55:
##                thrusters.clear()
##
            control.create_buttons()       
            bg.bgupdate(camx, camy)
            player.update(dt)
            player.offset2()
            nme.update(dt)
            nme2.update(dt)
            pg.draw.rect(nme.image,(0,255,0), nme.rect)
            p.update()
            thrust.update(ang)
            #Variables created to shorten equation for final blit below personal preference to reduce one time long equations.
            # I think the equation might be used again with slight difference
            
            # With the camera being the same velocity set in the Player Class, now is the time to blit the math to the screen to
            # break free of the screen boundary, follow the player position always
           
          
           


            screen.blit(base, basepos)
            # the nme and other creations need the camera subtracted from for them to move independently
            # this took a long time to understand even after reading about it
            screen.blit(nme.image, nme.position - player.camera)
            screen.blit(nme2.image, nme2.position - player.camera)
          
            player_hits = 0
            vv = v1.distance_to(v2)
            vvv = v1.distance_to(v3)
            if v1.distance_to(v2) < 3000:
                nme.move_towards_player(pos, ang)
                nme2.move_towards_player(pos, ang)









                     
            if v1.distance_to(v2) <= 3:
                 hit_count += 1
                 print("nmehit:")                 
          
          
                 
            text9 = font.render("NME dist: " + str(vv), True, con.WHITE)
       
            screen.blit(text9, (con.WIDTH - 1100, con.HEIGHT - 700))
            text10 = font.render("NME dist: " + str(vvv), True, con.WHITE)
       
            screen.blit(text10, (con.WIDTH - 1100, con.HEIGHT - 720))
            text11 = font.render("NME pos: " + str(v2), True, con.WHITE)
       
            screen.blit(text11, (con.WIDTH - 1100, con.HEIGHT - 740))
            

            text12 = font.render("hits" + str(hit_count), True, con.WHITE)
                    
            screen.blit(text12, (con.WIDTH - 200, con.HEIGHT - 800))
            
            screen.blit(textsurface,(10, 50))
          
            screen.blit(player.image, pppos)
       
          

            
            pg.display.flip()

      
            
          
       

       


        pg.quit()


if __name__ == "__main__":
    main()
    

