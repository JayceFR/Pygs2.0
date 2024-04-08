class Tile:
  def __init__(self, type, variant, pos) -> None:
    self.type = type
    self.variant = variant
    self.pos = pos
  
  def getType(self):
    return self.type
  
  def getVariant(self):
    return self.variant

  def getPos(self):
    return self.pos
  
  