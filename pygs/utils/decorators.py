from pygs.ui.hud import Hud
import pygame
from pygame.locals import *
def pygs(function):
  def clean(self=None):
    run = True
    while run:
      function(self)
      surf = self.display.copy()
      if not self.full_screen:
        surf = pygame.transform.scale(surf, pygame.display.get_window_size())
      else:
        surf = pygame.transform.scale(surf, pygame.display.get_window_size())
      self.screen.blit(surf, (0,0))
      pygame.display.flip()
      run = self.hud.get_controls()['run']
    print("hello")
  return clean
