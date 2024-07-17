def progression(time, cooldown, property):
  return int(min(time / cooldown, 1) * property)