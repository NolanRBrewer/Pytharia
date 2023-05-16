import pygame
from math import sin
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        # general
        super().__init__(groups)
        # entity direction
        self.direction = pygame.math.Vector2()

    def movement(self, speed):
        '''
        multiplies pixel movement by the entity's speed stat. 
        arg: 
            entities speed attribute 
        '''
        if self.direction.magnitude() != 0:
            # Normalizes diagonal movement to prevent speed boosting diagonally.
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collison('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collison('vertical')
        self.rect.center = self.hitbox.center
    
    def flicker_alpha(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: 
            return 255
        else:
            return 0

    def damage_animate(self):
        if not self.vulnerable:
            # Flicker
            alpha = self.flicker_alpha()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
            
    def collison(self, direction):

        '''
        Checks for the direction of entity movement and if there is a collison to correctly place the entity
        in case of a collision.
        args:
            direction of entity movement 
        returns: 
            None, but corrects entity position according to direction at time of  collision.
        '''
        if direction == 'vertical':
            # horicontal collisions
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # right moverment
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # left movement
                        self.hitbox.top = sprite.hitbox.bottom
        if direction == 'horizontal':
            # horicontal collisions
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # right moverment
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # left movement
                        self.hitbox.left = sprite.hitbox.right 