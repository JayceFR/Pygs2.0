import pygame
import random
import math
import time 
from pygame.locals import *
class FireFly():
    def __init__(self, x, y, radius,w,h, glow_img) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = random.randint(0,360)
        self.angle_change_cooldown = random.randint(50,250)
        self.angel_change_last_update = 0
        self.w = w
        self.h = h
        self.glow_img = glow_img
        self.amt = random.random() * 20 + 20
        self.amt_change_cooldown = 4000
        self.amt_last_update = 0
    
    def move(self, time):
        if time - self.angel_change_last_update > self.angle_change_cooldown:
            self.angel_change_last_update = time
            self.angle += random.randint(-50,50)
            if self.angle > 360:
                self.angle = 0
        if time - self.amt_last_update > self.amt_change_cooldown:
            self.amt = random.random() * 20 + 20
            self.amt_last_update = time
        self.x += math.cos(math.radians(self.angle)) * 0.5
        self.y += math.sin(math.radians(self.angle)) * 0.5
    
    def draw(self, display, scroll, time):
        #pygame.draw.circle(display, (255, 255, 255), (self.x - scroll[0], self.y - scroll[1]), self.radius)
        wpos = ((self.x - scroll[0] * 1.2) % self.w, (self.y - scroll[1] * 1.2) % self.h)
        pygame.draw.circle(display, (255,255,255,2), wpos , self.radius)
        diameter =math.sin(self.amt * 0.2 + time) * 6 + 30
        glow_img = pygame.transform.scale(self.glow_img, (diameter, diameter))
        display.blit(glow_img, (wpos[0] - glow_img.get_width()//2, wpos[1] - glow_img.get_height()//2), special_flags=BLEND_RGBA_ADD)
        # display.blit(self.circle_surf(), (int(self.x- self.radius) - scroll[0], int(self.y - self.radius) - scroll[1]), special_flags=BLEND_RGB_ADD)
        # self.radius -= 10 
    
    def circle_surf(self):
        surf = pygame.Surface((self.radius * 4, self.radius * 4))
        pygame.draw.circle(surf, (0, 0, 50,0), (self.radius, self.radius ), self.radius)
        surf.set_colorkey((0, 0, 0,0))
        return surf
    

class Fireflies():
    def __init__(self, width_of_entire_game, height_of_entire_game, glow_img) -> None:
        self.width_of_entire_game = width_of_entire_game * 2
        self.height_of_entire_game = height_of_entire_game * 2
        self.fireflies = []
        self.start_time = time.time()
        for x in range(15):
            # self.fireflies.append(FireFly(random.randint(-100,self.width_of_entire_game)//2, random.randint(-100,self.height_of_entire_game)//2, 1))
            self.fireflies.append(FireFly(random.random() * width_of_entire_game, random.random() * height_of_entire_game, 1, width_of_entire_game, height_of_entire_game, glow_img))
            
    def recursive_call(self, t, display, scroll):
        for firefly in self.fireflies:
            firefly.move(t)
            firefly.draw(display, scroll, time.time() - self.start_time)
