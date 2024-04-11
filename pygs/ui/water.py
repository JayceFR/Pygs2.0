import pygame, numpy
from scipy.interpolate import interp1d
POINT = pygame.Vector2
from pygame.locals import *
pygame.init()
class Molecule():
  def __init__(self, pos) -> None:
    self.velocity = 0
    self.force = 0
    self.height = pos[1]
    self.target_height = pos[1]
    self.colliding = False
    self.k = 0.015
    self.dampening = 0.03
    self.rect = pygame.rect.Rect(pos[0], pos[1], 16,16)
  
  def update(self):
    x = self.height - self.target_height
    if abs(x) < 0.01:
      self.height = self.target_height
    loss = -self.dampening * self.velocity
    self.force = -self.k * x + loss
    self.velocity += self.force
    self.height = min(self.height + 40 , self.height + self.velocity)
    # self.rect.y = self.height
  
  def draw(self, display, scroll):
    pygame.draw.circle(display, (0,0,255), (self.rect.x - scroll[0], self.height - scroll[1]), 4)

class Water():
  def __init__(self, pos, number_of_molecules, height, separation = 4) -> None:
    self.pos = pos
    self.molecules = []
    self.spread = 0.2
    self.spread = self.spread / 100
    self.height = height - 1
    self.passes = 8
    self.bottom = pos[1] + 1000
    self.number_of_molecules = number_of_molecules
    self.radius = separation
    for x in range(number_of_molecules + 1):
      self.molecules.append(Molecule((pos[0] + self.radius*x, pos[1])))
    # self.splash(7,20)
    self.points = []
  
  def update(self, scroll, player_rect):
    for pos, molecule in enumerate(self.molecules):
      if molecule.rect.colliderect(player_rect):
        if not molecule.colliding:
          molecule.colliding = True
          if player_rect.y > molecule.rect.y:
            self.splash(pos, -4)
          else:
            self.splash(pos, 4)
      else:
        if molecule.colliding:
          molecule.colliding = False
      molecule.update()
    self.spread_wave()
    self.points = [POINT(self.pos[0] - scroll[0], self.pos[1] + self.height - scroll[1])]
    for molecule in self.molecules:
      self.points.append(POINT(molecule.rect.x - scroll[0], molecule.height - scroll[1]))
    self.points.append(POINT(self.pos[0] + self.radius * (self.number_of_molecules + 1) - scroll[0], self.pos[1] + self.height - scroll[1]))
    # self.points = self.get_curve(self.points)
    # self.points.extend([POINT(self.pos[0] + self.radius * (self.number_of_molecules-1) - 16 - scroll[0], self.pos[1] + self.height - scroll[1]), POINT(self.pos[0] - scroll[0], self.pos[1] + self.height - scroll[1])])
    
  def spread_wave(self):
    spread = 0.08
    for i in range(len(self.molecules)):
        if i > 0:
            self.molecules[i - 1].velocity += spread * (self.molecules[i].height - self.molecules[i - 1].height)
        try:
            self.molecules[i + 1].velocity += spread * (self.molecules[i].height - self.molecules[i + 1].height)
        except IndexError:
            pass
    
  def splash(self, index, speed):
    if index >= 0 and index < len(self.molecules):
      self.molecules[index].velocity += speed
  
  def draw(self, display, scroll):
    new_surf = pygame.surface.Surface((1000,600))
    pygame.draw.polygon(new_surf, (0, 0, 255), self.points)
    new_surf.set_colorkey((0,0,0))
    pygame.draw.lines(display, (255,255,255), False, self.points[1:-1])
    display.blit(new_surf, (0,0), special_flags=BLEND_RGBA_ADD)

  def get_curve(self, points):
    x_new = numpy.arange(points[0].x, points[-1].x, 1)
    x = numpy.array([i.x for i in points[:-1]])
    y = numpy.array([i.y for i in points[:-1]])
    f = interp1d(x, y, kind='cubic', fill_value='extrapolate')
    y_new = f(x_new)
    x1 = list(x_new)
    y1 = list(y_new)
    points = [POINT(x1[i], y1[i]) for i in range(len(x1))]
    return points