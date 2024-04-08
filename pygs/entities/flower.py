import pygame, math, random
class Flower:
  def __init__(self, pos, img):
    self.pos  = pos
    self.img = img
    self.angle = 0
    self.scale = random.randint(1,7)
    self.target_angle = 0
  
  def render(self, surf, scroll):
    self.angle += (self.target_angle - self.angle) / 3
    img = self.img.copy()
    img = pygame.transform.rotate(img, self.angle)
    surf.blit(img, (self.pos[0] - scroll[0] - int(img.get_width()//2), self.pos[1] - scroll[1] - int(img.get_height()//2)))
  
  def collide(self, rect, time, gust):
    self.target_angle = 0
    self.target_angle += gust
    if abs(rect.bottom - self.pos[1]) < 20:
      rect_pos = [rect.center[0], rect.bottom]
      distance = math.sqrt((rect_pos[0] - self.pos[0]) ** 2 + (rect_pos[1] - self.pos[1]) ** 2)
      h_dis = rect_pos[0] - self.pos[0]
      if distance < 20:
        temp_target = 0
        if h_dis <= 0:
          temp_target = -70 - h_dis * 3.5
        if h_dis > 0:
          temp_target = 70 - h_dis * 3.5
        self.target_angle = min(self.target_angle + temp_target, 90)
        self.target_angle = max(self.target_angle, -90)
    if gust != 0:
      self.target_angle = self.target_angle + math.sin(time * 0.001 * self.scale ) * 6

class Flowers:
  def __init__(self, objs, assets, game):
    self.flowers = []
    self.flower_loc = {}
    for obj in objs:
      grid_loc = (int((obj['pos'][0] + 16) // game.tilemap.tile_size), int((obj['pos'][1] + 16) // game.tilemap.tile_size))
      if self.flower_loc.get(str(grid_loc[0]) + ";" + str(grid_loc[1])):
        self.flower_loc[str(grid_loc[0]) + ";" + str(grid_loc[1])].append(Flower((obj['pos'][0] + 16, obj['pos'][1] + 16), assets['flower'][obj['variant']]))
      else:
        self.flower_loc[str(grid_loc[0]) + ";" + str(grid_loc[1])] = [Flower((obj['pos'][0] + 16, obj['pos'][1] + 16), assets['flower'][obj['variant']])]
      # self.flowers.append(Flower((obj['pos'][0] + 16, obj['pos'][1] + 16), assets['flower'][obj['variant']]))
    print(self.flower_loc)
    self.flower_pos_list = list(self.flower_loc)
  
  def update(self, rect, surf, scroll, time, gust):
    # for flower in self.flowers:
    #   flower.collide(rect, time, gust)
    #   flower.render(surf, scroll)
    for pos in self.flower_pos_list:
      for flower in self.flower_loc[pos]:
        flower.collide(rect, time, gust)
        flower.render(surf, scroll)