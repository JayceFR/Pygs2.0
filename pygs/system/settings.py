import pygame, json, random
from ..utils.game_math import progression
from ..system.typewriter import TypeWriter

class Settings():
  def __init__(self, font, game) -> None:
    self.path = "data\save\settings.json"
    self.controls_keyboard = {}
    self.music = {}
    self.font = font
    self.game = game
    self.curr_hover_pos = -1
    self.resolutions = [["Enter Full Screen", None], ["384x216", (384, 216)], ["768x432", (768, 432)], ["1152x648", (1152, 648)], ["1536x684", (1536,684)], ["1920x1080", (1920, 1080)]]
    for x in range(len(self.resolutions)):
      self.resolutions[x].append(pygame.rect.Rect(10, 50 + x * 25, 150, 39))
      self.resolutions[x].append(pygame.rect.Rect(11, 50 + x * 25 + 3 , 146, 35))
      self.resolutions[x].append(False)
    
    # self.resolutions[random.randint(0,len(self.resolutions) - 1)][4] = True
    self.load()
  
  def default_conf(self):
    return {
      "controls_keyboard" : {
        "left" : [pygame.K_LEFT, pygame.K_a],
        "right" : [pygame.K_RIGHT, pygame.K_d],
        "up" : [pygame.K_UP, pygame.K_w],
        "down" : [pygame.K_DOWN, pygame.K_s],
        "jump" : [pygame.K_SPACE, pygame.K_UP, pygame.K_w],
        "dash" : [pygame.K_e, pygame.K_l],
        "fullscreen" : [pygame.K_f, pygame.K_ESCAPE]
      },
      "music" : {
        "volume" : 40
      },
    }

  def convert_to_set(self, dict):
    return_dict = {}
    for key in dict.keys():
      return_dict[key] = set(dict[key]) 
    return return_dict
  
  def convert_to_dict(self, pdict):
    return_dict = {}
    for key in pdict.keys():
      return_dict[key] = list(pdict[key]) 
    return return_dict

  def load(self):
    try:
      file = open(self.path, "r")
      settings = json.load(file)
      file.close()
      self.controls_keyboard = self.convert_to_set(settings["controls_keyboard"])
      self.music = settings["music"]
    except:
      conf = self.default_conf()
      self.controls_keyboard = self.convert_to_set(conf["controls_keyboard"])
      self.music = conf["music"] 
  
  def render(self, display, time):
    display.fill((0,0,0,0.5))
    #outline
    set_rect = pygame.rect.Rect(4, 4, progression(time, 1500, 90) , 30)
    controls_rect = pygame.rect.Rect(95, 4, progression(time, 1500, 90), 30)
    pygame.draw.rect(display, (200,200,200), set_rect, border_bottom_right_radius=10)
    pygame.draw.rect(display, (200,200,200), controls_rect, border_bottom_right_radius=10)
    #inner
    iset_rect = pygame.rect.Rect(5, 5, progression(time, 1000, 87), 26)
    pygame.draw.rect(display, (10,10,10), iset_rect, border_bottom_right_radius=10)
    icontrols_rect = pygame.rect.Rect(96, 5, progression(time, 1000, 87), 26)
    pygame.draw.rect(display, (10,10,10), icontrols_rect, border_bottom_right_radius=10)
    #typer
    img = self.font.render("Display", True, (255,255,255))
    display .blit(img, (14,4))
    img2 = self.font.render("Controls", True, (255,255,255))
    display.blit(img2, (98, 4))
    self.render_settings(display, time)
    display.set_colorkey((0,0,0,0))
  
  def render_settings(self, display, time):
    
    mouse_pos = list(pygame.mouse.get_pos())
    mouse_pos[0] /= 2
    mouse_pos[1] /= 2

    self.curr_hover_pos = -1

    if pygame.display.is_fullscreen():
      self.resolutions[0][0] = "Windowed Mode"
    else:
      self.resolutions[0][0] = "Enter Full Screen"

    for pos, res in enumerate(self.resolutions):
      if res[2].collidepoint(mouse_pos):
        self.curr_hover_pos = pos

    for pos, res in enumerate(self.resolutions):
      if pos != self.curr_hover_pos:
        pygame.draw.rect(display, (200,200,200), res[2], border_bottom_left_radius=10, border_top_right_radius=10)
        pygame.draw.rect(display, (10, 10,10), res[3], border_bottom_left_radius=9, border_top_right_radius=9)
        img = self.font.render(res[0], True, (255,255,255))
        display.blit(img, (res[3].x + 6, res[3].y + 2))
    
    if self.curr_hover_pos != -1:
      pygame.draw.rect(display, (10,200,10), self.resolutions[self.curr_hover_pos][2], border_bottom_left_radius=10, border_top_right_radius=10)
      pygame.draw.rect(display, (10, 10,10), self.resolutions[self.curr_hover_pos][3], border_bottom_left_radius=9, border_top_right_radius=9)
      img = self.font.render(self.resolutions[self.curr_hover_pos][0], True, (255,255,255))
      display.blit(img, (self.resolutions[self.curr_hover_pos][3].x + 6, self.resolutions[self.curr_hover_pos][3].y + 2))
    
    
  def save(self):
    file = open(self.path, "w")
    json.dump({"controls_keyboard" : self.convert_to_dict(self.controls_keyboard), "music" : self.music}, file)
    file.close()
