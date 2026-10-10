  elif event.type == pg.VIDEORESIZE:
                    screen = pg.display.set_mode(event.dict['size'], pg.DOUBLEBUF | pg.HWSURFACE | pg.RESIZABLE)
                    displaysurf = pg.transform.smoothscale(screen, screen_rect.size)
                       


                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                            zoom = 2
                            camx, camy = pcam
                            left   = camx + (screen_rect.left - camx) * zoom
                            right  = camx + (screen_rect.right - camx) * zoom
                            top    = camy + (screen_rect.top - camy) * zoom
                            bottom = camy + (screen_rect.bottom - camy) * zoom
                            screenrect = pg.Rect(left, top, right-left, bottom-top)
                            displaysurf = pg.transform.smoothscale(screen, screen_rect.size)
                    elif event.key == pg.K_x:
                            zoom = 0.5
                            
