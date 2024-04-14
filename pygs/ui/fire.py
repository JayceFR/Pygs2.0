import pygame, random
class FireParticle():
  def __init__(self, pos, radius=2) -> None:
    self.pos = list(pos)
    self.radius = radius
    self.orig_radius = radius
    self.alpha_layers = 2
    self.alpha_glow = 1.5
    max_srf_size = 2 * self.radius * self.alpha_layers * self.alpha_layers * self.alpha_glow
    self.surf = pygame.Surface((max_srf_size, max_srf_size), pygame.SRCALPHA)
    self.burn_rate = 0.1 * random.randint(1, 4)
  
  def draw(self, surf, scroll):
    max_srf_size = 2 * self.radius * self.alpha_layers * self.alpha_layers * self.alpha_glow
    self.surf = pygame.Surface((max_srf_size, max_srf_size), pygame.SRCALPHA)
    for x in range(self.alpha_layers, -1, -1):
      alpha = max(255 - x * (255//self.alpha_layers - 5), 0)
      radius = self.radius * x * x * self.alpha_glow
      if self.orig_radius >= 2.5:
        r,g,b = (255,0,0)
      elif self.orig_radius >= 1.5:
        r,g,b = (255, 150, 0)
      elif self.orig_radius >= 1:
        r,g,b = (120,120,120)
      else:
        r,g,b = (55,50,50)
      color = (r,g,b,alpha)
      pygame.draw.circle(self.surf, color, (self.surf.get_width()//2, self.surf.get_height()//2), radius)
    surf.blit(self.surf, self.surf.get_rect(center=(self.pos[0] -scroll[0] , self.pos[1] - scroll[1])))

  def update(self):
    self.pos[1] -= random.randint(2,5) - self.radius
    self.pos[0] += random.randint(-self.radius, self.radius)
    self.orig_radius -= self.burn_rate
    self.radius = int(self.orig_radius)
    if self.radius <= 0:
      self.radius = 0

class Flame():
  def __init__(self, pos) -> None:
    self.pos = pos
    self.x = pos[0]
    self.y = pos[1]
    self.flame_intensity = 2 
    self.flame_particles = []
    for i in range(self.flame_intensity * 25):
      self.flame_particles.append(FireParticle((self.x + random.randint(-3,3), self.y), random.randint(1,3)))
  
  def draw_flame(self, surf, scroll):
    for i in self.flame_particles:
      if i.radius <=0:
        self.flame_particles.remove(i)
        self.flame_particles.append(FireParticle((self.x + random.randint(-3,3), self.y), random.randint(1,3)))
        del i
        continue
      i.update()
      i.draw(surf, scroll)
