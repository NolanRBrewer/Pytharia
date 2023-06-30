import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'objects':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]- TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.hitbox_type()
        
    def hitbox_type(self):
        hitbox = self.rect
        if self.sprite_type == 'invisible':
            hitbox =  self.rect.inflate(0,HITBOX_OFFSET['invisible'])
        if self.sprite_type == 'bushes':
            hitbox = self.rect.inflate(0,HITBOX_OFFSET['bushes'])
        if self.sprite_type == 'objects':
            hitbox = self.rect.inflate(0,HITBOX_OFFSET['objects'])
        return hitbox