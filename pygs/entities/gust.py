import random
class Gust:
  def __init__(self) -> None:
    self.gust = 0
    self.target_gust = 0
    self.gust_choice = [-40, -20, 0, 0, 0, 20, 40]
    self.gust_update_cooldown = 4000
    self.gust_last_update = 0
  
  def update(self, time):
    #update gust
    self.gust += (self.target_gust - self.gust) // 3
    if time - self.gust_last_update > self.gust_update_cooldown:
      if self.target_gust < 0 or self.target_gust > 0:
        self.target_gust = 0
        if random.randint(0,3) == 0:
          self.gust = 0
      else:
        self.target_gust = self.gust_choice[random.randint(0, len(self.gust_choice)-1)]
      self.gust_last_update = time
  
  def wind(self):
    return self.gust