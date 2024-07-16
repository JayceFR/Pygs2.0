import pygame, json

class Settings():
  def __init__(self) -> None:
    self.path = "data\save\settings.json"
    self.controls_keyboard = {}
    self.music = {}
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

  def save(self):
    file = open(self.path, "w")
    json.dump({"controls_keyboard" : self.convert_to_dict(self.controls_keyboard), "music" : self.music}, file)
    file.close()
