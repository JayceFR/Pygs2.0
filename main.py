import pygame
from pygs.entities.gust import Gust
from pygs.entities.player import Player
from pygs.entities.flower import Flowers
from pygs.utils.images import load_img, load_imgs, load_spritesheet, Animation
from pygs.ui.hud import Hud
from pygs.map.map import TileMap

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Game():
  def __init__(self):
    self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    self.display = pygame.Surface((SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
    self.movement = [False, False]

    self.assets = {
      'player' : load_img('entities/player/player.png', scale=0.8),
      'grass' : load_imgs('tiles/grass', scale=1),
      'decor': load_imgs('tiles/decor', scale=1),
      'stone': load_imgs('tiles/stone', scale=1),
      'flower': load_imgs('tiles/flower', (255,255,255)),
      'player/idle': Animation(load_spritesheet('entities/player/idle.png', 4, scale=0.8, color_key=(255,255,255)), img_dur=10),
      'player/run': Animation(load_spritesheet('entities/player/run.png', 4, scale=0.8, color_key=(0,0,0)), img_dur=10),
      'player/jump': Animation([load_img('entities/player/jump.png', scale=0.8),])
    }

    print(self.assets)

    self.hud = Hud(self)

    self.clock = pygame.time.Clock()
    self.player = Player(self, [100,50], [self.assets['player'].get_width(),self.assets['player'].get_height()])

    self.tilemap = TileMap(self, tile_size=16)
    self.tilemap.load('map.json')

    flower_objs = self.tilemap.get_objs('flower')
    self.flower = Flowers(flower_objs, self.assets, self)
    self.gust = Gust()
    
    self.true_scroll = [0,0]
    # self.scroll = [0,0]

  def run(self):
    run = True
    while run:
      self.clock.tick(60)
      time = pygame.time.get_ticks()
      # print(self.clock.get_fps())
      self.display.fill((0,0,0))

      self.true_scroll[0] += (self.player.rect().x - self.true_scroll[0] - SCREEN_WIDTH//4) / 30
      self.true_scroll[1] += (self.player.rect().y - self.true_scroll[1] - SCREEN_HEIGHT//4) / 30
      scroll = self.true_scroll.copy()
      scroll[0] = int(scroll[0])
      scroll[1] = int(scroll[1])

      self.tilemap.render(self.display, scroll)

      self.flower.update(self.player.rect(), self.display, scroll, time, self.gust.wind())

      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
      self.player.render(self.display, scroll)

      self.gust.update(time)

      self.hud.events()
      controls = self.hud.get_controls()
      self.movement = [False, False]
      if controls['left'] :
        self.movement[0] = True
      if controls['right']:
        self.movement[1] = True
      if controls['jump']:
        self.player.velocity[1] = -3
      
      surf = self.display.copy()
      surf = pygame.transform.scale(surf, (SCREEN_WIDTH,SCREEN_HEIGHT))
      self.screen.blit(surf, (0,0))
      pygame.display.flip()
      run = controls['run']

Game().run()
