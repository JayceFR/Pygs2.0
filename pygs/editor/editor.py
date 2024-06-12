import pygame


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from pygs.utils.images import load_imgs
from pygs.ui.hud import Hud
from pygs.map.map import TileMap

RENDER_SCALE = 2.0

class Editor():
  def __init__(self):
    self.screen = pygame.display.set_mode((1000,600))
    pygame.display.set_caption("Editor")
    self.display = pygame.Surface((500,300))
    self.movement = [False, False, False, False]

    self.assets = {
      'grass' : load_imgs('tiles/grass', scale=1),
      'decor': load_imgs('tiles/decor', scale=1, color_key=(255,255,255)),
      'lamp': load_imgs('tiles/lamp', scale=2, color_key=(255,255,255)),
      'stone': load_imgs('tiles/stone', scale=1),
      'flower': load_imgs('tiles/flower', (255,255,255)),
      'spawners': load_imgs('tiles/spawners', (0,0,0)),
    }

    self.hud = Hud(self)
    print(self.__class__)

    self.clock = pygame.time.Clock()

    self.tilemap = TileMap(self, tile_size=16)

    try:
      self.tilemap.load("map.json")
    except FileNotFoundError:
      pass
    
    self.scroll = [-100,0]

    self.tile_list = list(self.assets)

    self.tile_group = 0
    self.tile_variant = 0

    self.clicking = False
    self.right_clicking = False

    self.ongrid = True
    self.mouse_pos = []

  def draw_text(self, text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))
  
  def toggle_offgrid(self):
    self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (self.mouse_pos[0] + self.scroll[0], self.mouse_pos[1] + self.scroll[1])})

  def run(self):
    run = True
    scroll_rect = pygame.rect.Rect(72,48,6,70)
    dir_rect = pygame.rect.Rect(5,5,15,15)
    orig_y = 48
    max_height = 170
    min_height = 70
    scroll_hover = False
    dir_hover = False
    dir_click = False
    control_scroll = False
    check = False
    scroll_bar_scroll = 0
    hover_ellipse = -1
    hover_tile = -1
    font = pygame.font.Font("data/font/jayce.ttf", 20)
    while run:
      self.clock.tick(60)
      self.display.fill((0,0,0))

      self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
      self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
      self.tilemap.render(self.display, render_scroll)

      self.mouse_pos = [pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1]/2]
      tile_pos = (int((self.mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size), int((self.mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size))
      
      if self.clicking and self.ongrid:
        self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
      if self.right_clicking:
        tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
        if tile_loc in self.tilemap.tilemap:
          del self.tilemap.tilemap[tile_loc]
        for tile in self.tilemap.offgrid_tiles.copy():
          tile_img = self.assets[tile['type']][tile['variant']]
          tile_r = pygame.rect.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
          if tile_r.collidepoint(self.mouse_pos):
            self.tilemap.offgrid_tiles.remove(tile)

      scroll_bar_scroll = (scroll_rect.y - 48) * 2 * (len(self.assets[self.tile_list[self.tile_group]]) - 1) // 5

      #Left Pane
      pygame.draw.rect(self.display, (20,20,20), pygame.rect.Rect(0,0,100,600))
      pygame.draw.rect(self.display, (30,30,30), (30, 35, 50, 200), border_radius=20)
      pygame.draw.rect(self.display, (100,20,0), (70, 45, 10, 178 ), border_radius=20)

      if scroll_rect.collidepoint(self.mouse_pos):
        scroll_hover = True
        pygame.draw.rect(self.display, (180,180,180), scroll_rect, border_radius=20)
      else:
        scroll_hover = False
        pygame.draw.rect(self.display, (155,155,155), scroll_rect, border_radius=20)
      
      if self.ongrid:
        pygame.draw.rect(self.display, (100,250,100), (50,7,30,12), border_radius=15)
      else:
        pygame.draw.rect(self.display, (250,100,100), (50,7,30,12), border_radius=15)
      
      if dir_rect.collidepoint(self.mouse_pos):
        dir_hover = True
      else:
        dir_hover = False
      
      hover_tile = -1
      for pos, img in enumerate(self.assets[self.tile_list[self.tile_group]]):
        curr_img = img.copy()
        if pos * 40 + 50 - int(scroll_bar_scroll) > 30 and pos * 40 + 50 - int(scroll_bar_scroll) < 220:
          if pygame.rect.Rect(45, pos * 40 + 50 - int(scroll_bar_scroll), curr_img.get_width(),curr_img.get_height()).collidepoint(self.mouse_pos):
            hover_tile = pos
          self.display.blit(curr_img, (45, pos * 40 + 50 - int(scroll_bar_scroll)))

      #Make this calculation when changing directory
      no_of_images = len(self.assets[self.tile_list[self.tile_group]])
      if no_of_images <= 5:
        scroll_rect.height = max_height
      else:
        scroll_rect.height = min_height

      current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
      current_tile_img.set_alpha(100)
      self.display.blit(current_tile_img, (105,5))
      if self.ongrid:
        self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
      else:
        self.display.blit(current_tile_img, self.mouse_pos)

      if dir_rect.collidepoint(self.mouse_pos):
        pygame.draw.ellipse(self.display, (170,180,250), dir_rect)
      else:
        pygame.draw.ellipse(self.display, (120,130,200), dir_rect)
      
      hover_ellipse = -1
      if dir_click:
        pygame.draw.line(self.display, (200,200,150), ( dir_rect.x + dir_rect.width//2 ,dir_rect.y + dir_rect.height), (dir_rect.x + dir_rect.width//2, dir_rect.y + 20 * len(self.tile_list) + 35))
        for x in range(len(self.tile_list)):
          if pygame.rect.Rect(7,20*x + 40,10,10).collidepoint(self.mouse_pos):
            hover_ellipse = x
            pygame.draw.ellipse(self.display, (150,200,150), pygame.rect.Rect(7,20*x + 40,10,10))
          else:
            pygame.draw.ellipse(self.display, (100,150,100), pygame.rect.Rect(7,20*x + 40,10,10))

      self.hud.events()
      controls = self.hud.get_controls()
      self.movement = [False, False, False, False]

      if controls['l_click']:
          if pygame.rect.Rect(0,0,100,600).collidepoint(self.mouse_pos):
            #left pane
            #scroll
            if scroll_hover:
              control_scroll = True
            #dir change
            if not check:
              if dir_click:
                dir_click = False
                check = True
              else:
                if dir_hover:
                  dir_click = True
                  check = True
            if hover_ellipse > -1:
              self.tile_group = hover_ellipse
              self.tile_variant = 0
              scroll_rect.y = orig_y
            if hover_tile > -1:
              self.tile_variant = hover_tile
          else:
            #right pane
            self.clicking = True
      else:
        check = False
        if control_scroll:
          control_scroll = False
        self.clicking = False
      
      if controls['r_click']:
        self.right_clicking = True
      else:
        self.right_clicking = False
      
      self.ongrid = controls['ongrid']
      
      if control_scroll:
        scroll_rect.y = min(218 - scroll_rect.height, max(self.mouse_pos[1] - scroll_rect.height // 2, 48))

      #write the name of dir
      if hover_ellipse > -1:
        self.draw_text(self.tile_list[hover_ellipse], font, (250,250,250), 6,250, self.display)

      if controls['left'] :
        self.movement[0] = True
      if controls['right']:
        self.movement[1] = True
      if controls['up']:
        self.movement[2] = True
      if controls['down']:
        self.movement[3] = True
      surf = self.display.copy()
      surf = pygame.transform.scale(surf, (1000,600))
      self.screen.blit(surf, (0,0))
      pygame.display.flip()
      run = controls['run']

Editor().run()
