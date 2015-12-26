#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
015_more_sprites.py
pygame sprites with hitbars and exploding fragments
url: http://thepythongamebook.com/en:part2:pygame:step015
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

pygame sprites moving araound and exploding into little fragments 
(on mouseclick). Effect of gravity on the fragments can be toggled.
Differnt coding style and its outcome on performance (framerate)
can be toggled and is displayed by green bars. a long bar indicates
a slow performance.

works with pyhton3.4 and python2.7
"""

#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division


def game():
        
    import pygame
    import os
    import random
    import math

    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()
    screen=pygame.display.set_mode((800,480)) # try out larger values and see what happens !
    winstyle = 0  # |FULLSCREEN # Set the display mode
    BIRDSPEEDMAX = 200
    BIRDSPEEDMIN = 10
    FRICTION =.999
    HITPOINTS = 100.0 
    FORCE_OF_GRAVITY = 9.81 # in pixel per second² .See http://en.wikipedia.org/wiki/Gravitational_acceleration
    print(pygame.ver)
    def write(msg="pygame is cool",size=32,color=(128,128,128)):
        """write text into pygame surfaces"""
        myfont = pygame.font.SysFont("None", size)
        mytext = myfont.render(msg, True, color)
        mytext = mytext.convert_alpha()
        return mytext
    
    #define sprite groups
    textgroup = pygame.sprite.LayeredUpdates()   
    bargroup = pygame.sprite.Group()
    #gaugegroup = pygame.sprite.Group()
    needlegroup = pygame.sprite.LayeredUpdates()
    # LayeredUpdates instead of group to draw in correct order
    allgroup = pygame.sprite.LayeredUpdates() # more sophisticated than simple group
    
    def loadimage(name):
        try:
            image = pygame.image.load(os.path.join("data",name))
            return image
        except:
            raise(UserWarning, "no image files %s  in subfolder 'data'"%name)

    class Gauge(object):
        
        def __init__(self,name,unit,startpos=screen.get_rect().center,backname="C1_trans240x240.png"):
            #pygame.sprite.Sprite.__init__(self, self.groups)
            self.name = name
            self.unit = unit
            self.x,self.y=0,0
            self.value = -9999
            self.oldvalue = -9999
            self.startpos = startpos
            mybackground = loadimage(backname)
            
            self.rect = mybackground.get_rect()
            self.rect.topleft = startpos

            mybackground.blit(write(name,size=18,color=(200,200,200)),(100,40))
            mybackground.blit(write(unit,size=18,color=(200,200,200)),(100,180))
            background.blit(mybackground,startpos)
            background.blit(write("Gauge",color=(255,0,0)), (50,300))
               
 
        def getBackground(self):
            return self.background;
        

        def setValue(self,v):
            self.text.setValue(v)

        
    
    class DigitGauge(Gauge):
        def __init__(self,name,unit,startpos=screen.get_rect().center,backname="C1_trans240x240.png"):
            super(DigitGauge,self).__init__(name,unit,startpos,backname)
            self.text = DigitGaugeText(self)
            self.text.rect.center = self.rect.center
        
    class DigitGaugeText(pygame.sprite.Sprite):
        def __init__(self,boss):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.value = 0
            self.oldvalue = -9999
            self.image=write("%.2f"%self.value,color=(250,250,250),size=48)
            self.rect = self.image.get_rect();
            self.boss = boss
            
        def setValue(self,v):
            self.oldvalue = self.value
            self.value = v
            
        
        def update(self, seconds):
            #self.value = clock.get_fps()
            if self.oldvalue != self.value:
                #self.image.fill(pygame.Color(5,5,5), (120, 100, 120, 50))
                #self.image.blit(self.background,(0,0))
                self.image=write("%.2f"%self.value,color=(250,250,250),size=48)
                self.rect = self.image.get_rect();
                x,y=self.boss.startpos
                #print( self.boss.rect)
                self.rect.center=self.boss.rect.center
                
    class AnalogGauge(Gauge):
        def __init__(self,name,unit,startpos=screen.get_rect().center,backname="C1_trans240x240.png"):
            super(self.__class__,self).__init__(name,unit,startpos,backname)
            self.needle = Needle(self)

            self.needle.rect.center = self.rect.center
            


    
    class Needle(pygame.sprite.Sprite):
        """needle of an instruement"""
        def __init__(self,boss):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.boss = boss
            
            
            self.image = pygame.image.load(os.path.join(".","380needle.png"))
            self.imageMaster = self.image
            self.rect = self.image.get_rect()
            #self.rect.center = (320, 240)
            
            self.angle = 0   # current direction
            self.target=0  # target direction
            self.r = 0

        def turnto(self,d):
            self.target = d 

        def turn(self, d):
            self.target = self.target + d

        def point_to(self,pos):
            x,y = pos
            dx = x - self.rect.centerx
            dy = y - self.rect.centery
            self.r = math.atan2(-dy,dx)
            angle = self.r/math.pi*180.0
            if angle < 0:
                angle = 360 + angle
            self.turnto(angle)


        def update(self, seconds):
            # no need for seconds but the other sprites need it
            #self.rect.midleft = pygame.mouse.get_pos()
            oldCenter = self.rect.center
            #self.image = pygame.transform.rotate(self.imageMaster, self.dir)
            
            #self.point_to(pygame.mouse.get_pos())
            diff = math.fabs(self.target - self.angle)
            if diff > 10: diff = 10
            if diff > 1:
                if self.target > self.angle:
                    self.angle += diff
                elif self.target < self.angle:
                    self.angle -= diff

                #self.angle = self.target
            

                self.image = pygame.transform.rotozoom(self.imageMaster,self.angle,1.0)
                # dx = math.cos(self.angle*math.pi/180)*100
                # dy = math.sin(self.angle*math.pi/180)*100
                self.rect = self.image.get_rect()
                self.rect.center=oldCenter
                #self.rect.center = (320+dx,240-dy)
                #self.dir = angle
                #print(dx,dy,angle)
                #print(dx,dy,self.angle)
                print(self.angle)

    
            
    class Timebar(pygame.sprite.Sprite):
        """shows a bar as long as how much milliseconds are passed between two frames"""
        def __init__(self, long):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.long = long   * 2
            self.image = pygame.Surface((self.long,5))
            self.image.fill((128,255,0))
            self.image.convert()
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (0,screen.get_height())
        
        def update(self, time):
            self.rect.centery = self.rect.centery - 7
            if self.rect.centery < 0:
                self.kill()

    
    
    #---------------  no class -----------
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.blit(loadimage("back_carbon.png"),(0,0))
    background.blit(write("%s"%background.get_rect()),(150,0))
    background.blit(write("press left mouse button for more sprites."),(150,10))
    background.blit(write("press right mouse button to kill sprites."),(150,40))
    background.blit(write("press g to toggle gravity"),(150,70))
    background.blit(write("press b to toggle bad coding"),(150,100))
    background.blit(write("press c to toggle clever coding"), (150,130))
    background.blit(write("Press ESC to quit"), (150,160))
	

    # paint vertical lines to measure passed time (Timebar)
    #for x in range(0,screen.get_width()+1,20):
    for x in range(0,140,20):
        pygame.draw.line(background, (255,0,255), (x,0) ,(x,screen.get_height()), 1)
    
    BLUE=(0,0,255)
    pygame.draw.line(background,BLUE,(320-2,240),(320+2,240),1)
    pygame.draw.line(background,BLUE,(320,240-2),(320,240+2),1)
 
   

    #assign default groups to each sprite class
    # (only allgroup is useful at the moment)
    Timebar.groups = bargroup, allgroup
    Needle.groups = needlegroup,allgroup
    DigitGaugeText.groups = textgroup,allgroup
    #assign default layer for each sprite (lower numer is background)
    Needle._layer = 6
    DigitGaugeText._layer=4
    Timebar._layer = 3


    fps = DigitGauge("Perf","fps",(50,0))
    
    #speedo= AnalogGauge("speed","km/h",(300,10),backname="C1_trans480x480.png")
    speedo= AnalogGauge("speed","km/h",(300,10),backname="C1_trans480x480.png")
    
    # at game start create a Needle
   
    #needle = Needle()
    degree = DigitGauge("Needle","degree",(50,240))
    
    # set 
    millimax = 0
    othergroup =  [] # important for good collision detection
    badcoding = False
    clevercoding = False
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second. 

    background = background.convert()  # jpg can not have transparency
    screen.blit(background, (0,0))     # blit background on screen (overwriting all)

    
    while mainloop:
        
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        Timebar(milliseconds)
        fps.setValue(clock.get_fps())
        degree.setValue(speedo.needle.angle)

        if milliseconds > millimax:
            millimax = milliseconds
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                elif event.key == pygame.K_p:
                    print("----------")
                    print("toplayer:", allgroup.get_top_layer())
                    print("bottomlayer:", allgroup.get_bottom_layer())
                    print("layers;", allgroup.layers())
                elif event.key == pygame.K_z:
                    speedo.needle.turn(5) # turn 5 degree clock
                elif event.key == pygame.K_x:
                    speedo.needle.turn(-5) # turn -5 degree
                elif event.key == pygame.K_v:
                    speedo.needle.turnto(270) # 270 degree, point down     
                elif event.key == pygame.K_f:
                    speedo.needle.turnto(90) # 90 degree, point up

        # turn to mouse left click
        if pygame.mouse.get_pressed()[0]:
            speedo.needle.point_to(pygame.mouse.get_pos())


        pygame.display.set_caption("ms: %i max(ms): %i fps: %.2f "% (milliseconds, millimax, clock.get_fps(), ))
        
                    
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        # pygame.draw.line(screen,BLUE,(320-2,240),(320+2,240),1)
        # pygame.draw.line(screen,BLUE,(320,240-2),(320,240+2),1)

        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    game()
