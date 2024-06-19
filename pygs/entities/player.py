import pygame, random, math
from .entity import PhysicsEntity
from ..ui.particle import Particle

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
    
    def update(self, tilemap, movement = (0,0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1

        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
        
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        if abs(self.dashing) in {40, 30}:
                for x in range(20):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 0.5 + 0.5
                    pvel = [math.cos(angle) * speed, math.sin(angle) * speed]
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvel, frame=random.randint(0,7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 30:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 31:
                self.velocity[0] *= 0.1
            pvel = [abs(self.dashing)/ self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvel, frame=random.randint(0,7)))

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
    
    def render(self, surf, offset=(0,0)):
        if abs(self.dashing) <= 30:
            super().render(surf, offset=offset)

    
    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 1.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -1.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity[1] -= 3
            self.jumps -= 1
            self.air_time = 5
    
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -40
            else:
                self.dashing = 40
