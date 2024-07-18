from pygs.ui.hud import Hud
from pygs.shader.shader import Shader
import pygame
import time
from pygame.locals import *

def pygs(function):
  def game(self=None):
    run = True
    uniform = {'noise_tex1': self.noise_img1, 'noise_tex2' : self.noise_img2}
    start_time = time.time()
    self.sfx['ambience'].play(-1)
    last_time = time.time()
    while run:
      self.dt = time.time() - last_time
      self.dt *= 60
      last_time = time.time()
      if self.settings_window:
        self.darkness = 0.8
      else:
        self.darkness = 0
      function(self)
      #particles
      for particle in self.particles.copy():
        kill = particle.update()
        particle.render(self.display, offset=self.scroll)
        if kill:
          self.particles.remove(particle)

      surf = self.display.copy()
      if not self.full_screen:
        surf = pygame.transform.scale(surf, pygame.display.get_window_size())
      else:
        surf = pygame.transform.scale(surf, pygame.display.get_window_size())
      self.screen.blit(surf, (0,0))
      uniform = {'noise_tex1': self.noise_img1, 'noise_tex2' : self.noise_img2, 'tex': self.screen, 'ui_tex' : self.ui_display}
      variables = {'itime' : time.time() - start_time, 'cam_scroll': tuple(list(self.scroll)), 'darkness': self.darkness}
      self.shader_obj.draw(uniform, variables)
      pygame.display.flip()
      run = self.hud.get_controls()['run']
    print("hello")
    self.settings.save()
  return game

