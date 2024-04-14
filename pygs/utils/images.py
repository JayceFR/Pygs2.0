import pygame, os

BASE_IMG_PATH = './data/images/'

#load a specific image
def load_img(path, color_key = (0,0,0), scale=0, scale_coords=None):
  curr_img = pygame.image.load(BASE_IMG_PATH + path).convert()
  if scale > 0 or scale_coords:
    if not scale_coords:
      curr_img = pygame.transform.scale(curr_img, (curr_img.get_width()*scale, curr_img.get_height()*scale))
    else:
      curr_img = pygame.transform.scale(curr_img, scale_coords)
  curr_img.set_colorkey(color_key)
  return curr_img

#load images from a folder
def load_imgs(path, color_key=(0,0,0), scale=0, scale_coords=None):
  images = []
  for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
    images.append(load_img(path + "/" + img_name, color_key=color_key, scale=scale, scale_coords=scale_coords))
  return images 

#load a spritesheet
def load_spritesheet(path, number_of_frames, scale = 0, color_key = (0,0,0), scale_coords = None):
  sheet = load_img(path).convert()
  width = sheet.get_width()
  height = sheet.get_height()
  animation = []
  for x in range(number_of_frames):
    image = pygame.Surface((width//number_of_frames, height)).convert()
    image.blit(sheet, (0,0), ((x * width//number_of_frames), 0, width//number_of_frames, height))
    if scale > 0:
      image = pygame.transform.scale(image, (image.get_width() * scale, height * scale))
    if scale_coords:
      image = pygame.transform.scale(image, scale_coords)
    image.set_colorkey(color_key)
    animation.append(image)
  return animation


class Animation:
  def __init__(self, images, img_dur=5, loop=True) -> None:
    self.images = images
    self.loop = loop
    self.img_duration = img_dur
    self.done = False
    self.frame = 0

  def copy(self):
    return Animation(self.images, self.img_duration, self.loop)
  
  def img(self):
    return self.images[int(self.frame/self.img_duration)]
  
  def update(self):
    if self.loop:
      self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
    else:
      self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
      if self.frame >= self.img_duration * len(self.images) - 1:
        self.done = True