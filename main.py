import pygame
from pygame.locals import *
from pygs.entities.gust import Gust
from pygs.entities.player import Player
from pygs.entities.citizien import Citizen
from pygs.entities.flower import Flowers
from pygs.ui.water import Water
from pygs.utils.images import load_img, load_imgs, load_spritesheet, Animation
from pygs.ui.hud import Hud
from pygs.map.map import TileMap


SCREEN_WIDTH = 1536 // 2
SCREEN_HEIGHT = 960 // 2

class Game():
  def __init__(self):
    pygame.display.set_caption("Pygs2.0")
    self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
    self.MONITOR_SIZE = pygame.display.get_desktop_sizes()[0]
    print(self.MONITOR_SIZE)
    self.display = pygame.Surface((SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
    self.movement = [False, False]

    self.assets = {
      'player' : load_img('entities/player/player3.png', scale=1),
      'grass' : load_imgs('tiles/grass', scale=1),
      'decor': load_imgs('tiles/decor', scale=1, color_key=(255,255,255)),
      'stone': load_imgs('tiles/stone', scale=1),
      'flower': load_imgs('tiles/flower', (255,255,255)),
      'citizen/idle' : Animation(load_spritesheet('entities/citizen/idle.png', 4, color_key=(0,0,0)), img_dur=7),
      'citizen/run': Animation(load_spritesheet('entities/citizen/run.png', 4, color_key=(0,0,0)), img_dur=6),
      'player/idle': Animation(load_spritesheet('entities/player/player3_idle.png', 2, scale=1, color_key=(255,255,255)), img_dur=15),
      # 'player/run': Animation(load_spritesheet('entities/player/run.png', 4, scale=0.8, color_key=(0,0,0)), img_dur=10),
      # 'player/idle': Animation([load_img('entities/player/player3.png', scale=1, color_key=(255,255,255)),]),
      'player/run': Animation([load_img('entities/player/player3.png', scale=1, color_key=(255,255,255)),]),
      'player/jump': Animation([load_img('entities/player/player3.png', scale=1, color_key=(255,255,255)),])
    }

    self.hud = Hud(self)

    self.clock = pygame.time.Clock()
    self.player = Player(self, [0,0], [self.assets['player'].get_width(),self.assets['player'].get_height()])

    self.tilemap = TileMap(self, tile_size=16)
    self.tilemap.load('map.json')

    flower_objs = self.tilemap.get_objs('flower')
    self.flower = Flowers(flower_objs, self.assets, self)
    self.gust = Gust()

    self.citizens = []
    self.water_pos = []
    for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2)]):
      if spawner['variant'] == 0:
        print(spawner['pos'])
        self.player.pos = spawner['pos']
      elif spawner['variant'] == 1:
        self.citizens.append(Citizen(self, spawner['pos'], (14,20)))
      elif spawner['variant'] == 2:
        self.water_pos.append(spawner['pos'])
    
    self.water_pos = sorted(self.water_pos)
    print(self.water_pos)
    self.waters_rects = []
    for pos in self.water_pos:
      if not self.waters_rects:
        #loop to check for the height
        found = True
        height = 0
        while found:
          if [pos[0], pos[1] + 16 * (height + 1)] in self.water_pos:
            self.water_pos.remove([pos[0], pos[1] + 16 * (height + 1)])
            height += 1
          else:
            found = False
        self.waters_rects.append([pos[0], pos[1], 16, 16 * (height + 1)])
      else:
        #check if the current tile lies consecutively after the previous
        #get the height
        found = True
        height = 0
        while found:
          if [pos[0], pos[1] + 16 * (height + 1)] in self.water_pos:
            self.water_pos.remove([pos[0], pos[1] + 16 * (height + 1)])
            height += 1
          else:
            found = False
        # print("I am here", height)
        if self.waters_rects[-1][0] + self.waters_rects[-1][2] == pos[0]:
          self.waters_rects[-1][2] += 16
          if (height + 1) * 16 > self.waters_rects[-1][3]:
            self.waters_rects[-1][3] = (height + 1) * 16
        else:
          self.waters_rects.append([pos[0], pos[1], 16, 16 * (height+1)])
    print(self.waters_rects)
    print(self.water_pos)
    self.waters = []
    for rect in self.waters_rects:
      self.waters.append(Water((rect[0], rect[1]), rect[2]//4, rect[3]))
    self.true_scroll = [0,0]
    self.full_screen = False
    # self.scroll = [0,0]

  def run(self):
    print(pygame.display.get_window_size())
    run = True
    while run:
      self.clock.tick(60)
      time = pygame.time.get_ticks()
      # print(self.clock.get_fps())
      self.display.fill((0,0,0))

      if not self.full_screen:
        self.true_scroll[0] += (self.player.rect().x - self.true_scroll[0] - pygame.display.get_window_size()[0]//4) / 30
        self.true_scroll[1] += (self.player.rect().y - self.true_scroll[1] - pygame.display.get_window_size()[1]//4) / 30
      else:
        self.true_scroll[0] += (self.player.rect().x - self.true_scroll[0] - pygame.display.get_window_size()[0]//4) / 30
        self.true_scroll[1] += (self.player.rect().y - self.true_scroll[1] - pygame.display.get_window_size()[1]//4) / 30
      scroll = self.true_scroll.copy()
      scroll[0] = int(scroll[0])
      scroll[1] = int(scroll[1])

      self.tilemap.render(self.display, scroll)

      self.flower.update(self.player.rect(), self.display, scroll, time, self.gust.wind())

      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
      self.player.render(self.display, scroll)

      # for rect in self.waters_rects:
      #   pygame.draw.rect(self.display, (0,0,200), [rect[0] - scroll[0], rect[1] - scroll[1], rect[2], rect[3]])

      for water in self.waters:
        water.update(scroll, self.player.rect())
        water.draw(self.display, scroll)

      for citizen in self.citizens:
        citizen.update(self.tilemap, (0,0))
        citizen.render(self.display, offset=scroll)

      self.gust.update(time)

      self.hud.events()
      controls = self.hud.get_controls()
      self.movement = [False, False]
      if controls['left'] :
        self.movement[0] = True
      if controls['right']:
        self.movement[1] = True
      
      surf = self.display.copy()
      if not self.full_screen:
        surf = pygame.transform.scale(surf, (SCREEN_WIDTH,SCREEN_HEIGHT))
      else:
        surf = pygame.transform.scale(surf, pygame.display.get_window_size())
      self.screen.blit(surf, (0,0))
      pygame.display.flip()
      run = controls['run']

Game().run()
