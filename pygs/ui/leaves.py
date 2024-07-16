import random
import pygame, math
class Leaf():
  def __init__(self,x ,y, img, w, h) -> None:
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.img = img 
    self.angle = random.randint(0,360)
    self.angle_dt = random.randint(250,450)
    self.angle_last_update = 0
    self.gravity = random.choice([1.1, 1.2, 1.3, 1.5, 0.5, 0.6, 0.7, 0.8])
  
  def move(self, time, gust, dt = 1):
    if time - self.angle_last_update > self.angle_dt:
      self.angle_last_update = time
      self.angle += random.randint(-50,50) % 360
    self.x += math.cos(math.radians(self.angle)) * 0.6 + gust * -0.07 * dt
    self.y += self.gravity * dt
  
  def draw(self, display, scroll):
    img = pygame.transform.rotate(self.img, self.angle)
    display.blit(img, ((self.x - scroll[0])%self.w, (self.y - scroll[1])%self.h))

class LeafManager():
  def __init__(self, width_of_screen, height_of_screen, img) -> None:
    self.w = width_of_screen
    self.h = height_of_screen
    self.leaves = []
    for x in range(10):
      self.leaves.append(Leaf(random.random() * self.w, random.random() * self.h, img, self.w, self.h))
  
  def recursive_call(self, time, display, scroll, gust, dt = 1):
    for leaf in self.leaves:
      leaf.move(time, gust, dt)
      leaf.draw(display, scroll)

    
