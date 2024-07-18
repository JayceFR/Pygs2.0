import pygame, random
from pygame.locals import *
from pygs.entities.gust import Gust
from pygs.entities.player import Player
from pygs.entities.citizien import Citizen
from pygs.entities.flower import Flowers
from pygs.ui.leaves import LeafManager
from pygs.ui.water import WaterManager
from pygs.ui.fireflies import Fireflies
from pygs.utils.images import load_img, load_imgs, load_spritesheet, Animation
from pygs.ui.hud import Hud
from pygs.map.map import TileMap
from pygs.utils.decorators import pygs
from pygs.ui.fire import Flame
from pygs.system.settings import Settings
from pygs.shader.shader import Shader

pygame.init()

class Game():
  def __init__(self):
    pygame.display.set_caption("Pygs2.0")
    self.settings = Settings(pygame.font.Font('./data/font/munro.ttf', 20), self)
    flags = pygame.OPENGL | pygame.DOUBLEBUF
    if self.settings.display["res"] != None:
      SCREEN_WIDTH = self.settings.display["res"][0]
      SCREEN_HEIGHT = self.settings.display["res"][1]
    else:
      SCREEN_WIDTH = 1280
      SCREEN_HEIGHT = 720
    self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags )
    if self.settings.display["res"] == None:
      pygame.display.toggle_fullscreen()
    self.display = pygame.Surface((640,360))
    self.ui_display = pygame.Surface((640, 360), pygame.SRCALPHA)
    self.movement = [False, False]

    self.assets = {
      'player' : load_img('entities/player/player.png', scale=0.8),
      'grass' : load_imgs('tiles/grass', scale=1),
      'boomerang' : load_img('entities/boomerang/0.png', scale=0.9),
      'decor': load_imgs('tiles/decor', scale=1, color_key=(255,255,255), args={'tree3.png':[1.5,None], 'tree4.png':[1.5,None]}),
      'stone': load_imgs('tiles/stone', scale=1),
      'lamp': load_imgs('tiles/lamp', scale=2, color_key=(255,255,255)),
      'flower': load_imgs('tiles/flower', (255,255,255)),
      'citizen/idle' : Animation(load_imgs('entities/citizen/idle'), img_dur=15),
      'citizen/run': Animation([load_img('entities/citizen/player3.png', scale=1, color_key=(255,255,255)),],),
      'player/idle' : Animation(load_imgs('entities/player/idle', scale=0.8), img_dur=10),
      'player/run' : Animation(load_imgs('entities/player/run', scale=0.8), img_dur=6),
      'player/jump': Animation(load_imgs('entities/player/jump', scale=0.8, color_key=(0,0,0))),
      'particles/particle' : Animation(load_imgs('particle', scale=2), img_dur=6, loop=False)
    }

    self.sfx = {
      'ambience': pygame.mixer.Sound('./data/music/ambience.wav')
    }

    self.sfx['ambience'].set_volume(0.05)

    print(self.assets['decor'][0].get_alpha())
    print(load_imgs('entities/citizen/idle')[0].get_alpha())

    self.hud = Hud(self)

    pygame.key.set_mods(0)

    self.clock = pygame.time.Clock()
    self.player = Player(self, [0,0], [self.assets['player'].get_width(),self.assets['player'].get_height()])
    # self.player = Player(self, [0,0], [12,])

    self.dt = 0

    self.tilemap = TileMap(self, tile_size=16)
    self.tilemap.load('map.json')

    self.fragment_loc = "./data/scripts/fragment.frag"
    self.vertex_loc = "./data/scripts/vertex.vert"
    self.noise_img1 = pygame.image.load('./data/images/misc/pnoise.png').convert_alpha()
    self.noise_img2 = pygame.image.load('./data/images/misc/pnoise2.png').convert_alpha()
    self.shader_obj = Shader(True, self.vertex_loc, self.fragment_loc)

    flower_objs = self.tilemap.get_objs('flower')
    self.flower = Flowers(flower_objs, self.assets, self)
    self.gust = Gust()

    self.scroll = []

    self.citizens = []
    self.water_pos = []
    self.fire_pos = []

    for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2)]):
      if spawner['variant'] == 0:
        self.player.pos = spawner['pos']
      elif spawner['variant'] == 1:
        self.citizens.append(Citizen(self, spawner['pos'], (12,29)))
      elif spawner['variant'] == 2:
        self.water_pos.append(spawner['pos'])
    
    self.water_manager = WaterManager()
    self.water_manager.load(self.water_pos, self)
    for fire_pos in self.tilemap.extract([('decor', 4),], True):
      self.fire_pos.append(fire_pos)

    self.glow_img = pygame.Surface((255,255))
    self.glow_img.fill((174*0.2, 226*0.2, 255*0.3))
    img = pygame.image.load('./data/images/misc/light.png').convert()
    self.glow_img.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    self.fireflies = Fireflies(self.display.get_width(),self.display.get_height(), self.glow_img)

    self.lamp_img = pygame.Surface((730, 1095))
    self.lamp_img.fill((255*0.6, 255*0.6, 255*0.6))
    lamp_img = pygame.image.load('./data/images/misc/lamp2.png').convert()
    self.lamp_img.blit(lamp_img, (0,0), special_flags=BLEND_RGBA_MULT)
    self.lamp_glow_img = pygame.Surface((255,255))
    self.lamp_glow_img.fill((255*0.3, 255*0.3, 255*0.3))
    self.lamp_glow_img.blit(img, (0,0), special_flags=BLEND_RGBA_MULT)
    self.lamp_glow_img = pygame.transform.scale(self.lamp_glow_img, (60,60))
    self.lamp_img = pygame.transform.scale(self.lamp_img, (self.lamp_img.get_width()//10, self.lamp_img.get_height()//10))

    self.lamp_positions = []
    for lamp_pos in self.tilemap.extract([('lamp',0),], True):
      self.lamp_positions.append(lamp_pos)

    leaf_img = pygame.image.load('./data/images/ui/leaf.png').convert()
    leaf_img.set_colorkey((0,0,0))
    self.leaf = LeafManager(self.display.get_width(), self.display.get_height(), leaf_img )
    
    self.particles = []

    self.true_scroll = [0,0]
    self.full_screen = False
    self.fire_particles = []
    for obj in self.fire_pos:
      self.fire_particles.append(Flame((obj['pos'][0] + 10, obj['pos'][1] + 2)))
    # self.scroll = [0,0]
    self.settings_window = False
    self.darkness = 0

  @pygs
  def run(self):
      self.clock.tick(60)
      time = pygame.time.get_ticks()
      # print(self.clock.get_fps())
      self.ui_display.fill((0,0,0,0))
      self.display.fill((2,2,2))

      controls = self.hud.get_controls()
      self.movement = [False, False]
      if not self.settings_window:
        if controls['left'] :
          self.movement[0] = True
        if controls['right']:
          self.movement[1] = True

      self.true_scroll[0] += (self.player.rect().x - self.true_scroll[0] - 1280//4) / 5
      self.true_scroll[1] += (self.player.rect().y - self.true_scroll[1] - 720//4) / 20

      self.scroll = self.true_scroll.copy()
      self.scroll[0] = int(self.scroll[0])
      self.scroll[1] = int(self.scroll[1])

      self.tilemap.render(self.display, self.scroll)

      self.flower.update(self.player.rect(), self.display, self.scroll, time, self.gust.wind())

      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0), self.dt)
      self.player.render(self.display, self.scroll)
      for particle in self.fire_particles:
        particle.draw_flame(self.display, self.scroll)

      self.water_manager.update(self)

      for citizen in self.citizens:
        citizen.update(self.tilemap, (0,0), self.dt)
        citizen.render(self.display, offset=self.scroll)

      if self.settings_window:
        self.settings.render(self.ui_display, time)
      
      #lamp img 
      for lamp in self.lamp_positions:
        pos = lamp['pos']
        self.display.blit(self.lamp_img, (pos[0] - self.scroll[0] - 24, pos[1] - self.scroll[1] + 30), special_flags=BLEND_RGBA_ADD)
        self.display.blit(self.lamp_glow_img, (pos[0] - self.scroll[0] - 17, pos[1] - self.scroll[1] - 10), special_flags=BLEND_RGBA_ADD)

      self.gust.update(time)
      self.fireflies.recursive_call(time, self.display, self.scroll, self.dt)
      self.leaf.recursive_call(time, self.display, self.scroll, self.gust.wind(), dt=self.dt)

      self.hud.events(self.settings.controls_keyboard)
      

Game().run()
