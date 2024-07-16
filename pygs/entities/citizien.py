from .entity import PhysicsEntity
import random

class Citizen(PhysicsEntity):
  def __init__(self, game, pos, size):
    super().__init__(game, 'citizen', pos, size)

    self.walking = 0
  
  def update(self, tilemap, movement=(0,0), dt=1):
    if self.walking:
      if tilemap.solid_check((self.rect().centerx + (-self.size[0]//2 if self.flip else self.size[0]//2), self.pos[1] + self.size[1])):
        if (self.collisions['right'] or self.collisions['left']):
          self.flip = not self.flip
        else:
          movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
      else:
        self.flip = not self.flip
      self.walking = max(0, self.walking-1)
    elif random.random() < 0.01:
      self.walking = random.randint(30,120)
    
    super().update(tilemap, movement=movement, dt=dt)

    if movement[0] != 0:
      self.set_action('run')
    else:
      self.set_action('idle')