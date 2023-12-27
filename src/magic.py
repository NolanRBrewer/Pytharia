import pygame
from settings import *

class Flame(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        # typing
        self.sprite_type = 'magic'
        # graphic
        full_path  = f'./level_graphics/magic/{player.spell}.png'
        #sound
        self.sfx = pygame.mixer.Sound(magic_data[player.spell]['attack_sound'])
        self.sfx.set_volume(0.2)

        # placement
        direction = player.status.split('_')[0]
        if player.mana >= magic_data[player.spell]['cost']:
            player.mana -= magic_data[player.spell]['cost']
            self.sfx.play()
            self.image = pygame.image.load(full_path).convert_alpha()
            if direction == 'right':
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-10,10))
            elif direction == 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(10,10))
            elif direction == 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,10))
            elif direction == 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(10,-10))
        else:
            self.image = pygame.image.load('./level_graphics/magic/fizzle.png')
            self.rect = self.image.get_rect(center = player.rect.center)

class Heal(pygame.sprite.Sprite):
    def __init__(self,player, groups):
        # general
        super().__init__(groups)
        # typing
        self.sprite_type = 'particle'
        # graphic
        full_path  = f'./level_graphics/magic/{player.spell}.png'
        #sound
        self.sfx = pygame.mixer.Sound(magic_data[player.spell]['attack_sound'])
        self.sfx.set_volume(0.2)

        if player.mana >= magic_data[player.spell]['cost']:
            self.sfx.play()
            self.image = pygame.image.load(full_path).convert_alpha()
            self.heal(player)
        else: 
            self.image = pygame.image.load('./level_graphics/magic/fizzle.png')
        self.rect = self.image.get_rect(center = player.rect.center)
        

    def heal(self,player): 
        player.health += magic_data[player.spell]['potency']
        player.mana -= magic_data[player.spell]['cost']
        if player.health >= player.stats['health']:
            player.health = player.stats['health']

class Bubble(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        # graphic
        full_path  = f'./level_graphics/magic/{player.spell}.png'
        #sound
        self.sfx = pygame.mixer.Sound(magic_data[player.spell]['attack_sound'])
        self.sfx.set_volume(0.2)
        # placement and valid casting
        direction = player.status.split('_')[0]
        if player.mana >= magic_data[player.spell]['cost']:
            player.mana -= magic_data[player.spell]['cost']
            self.sfx.play()
            self.image = pygame.image.load(full_path).convert_alpha()
            if direction == 'right':
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-10,10))
            elif direction == 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(10,10))
            elif direction == 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,10))
            elif direction == 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(10,-10))
        else:
            self.image = pygame.image.load('./level_graphics/magic/fizzle.png')
            self.rect = self.image.get_rect(center = player.rect.center)

class Snowfall(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        # graphic
        full_path  = f'./level_graphics/magic/{player.spell}.png'
        #sound
        self.sfx = pygame.mixer.Sound(magic_data[player.spell]['attack_sound'])
        self.sfx.set_volume(0.2)
        # placement and valid casting
        direction = player.status.split('_')[0]
        if player.mana >= magic_data[player.spell]['cost']:
            player.mana -= magic_data[player.spell]['cost']
            self.sfx.play()
            self.image = pygame.image.load(full_path).convert_alpha()
            if direction == 'right':
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-10,10))
            elif direction == 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(10,10))
            elif direction == 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,10))
            elif direction == 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(10,-10))
        else:
            self.image = pygame.image.load('./level_graphics/magic/fizzle.png')
            self.rect = self.image.get_rect(center = player.rect.center)

class Barrier(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = 'bush'
        # graphic
        full_path  = f'./level_graphics/magic/{player.spell}.png'
        #sound
        self.sfx = pygame.mixer.Sound(magic_data[player.spell]['attack_sound'])
        self.sfx.set_volume(0.2)
        # placement and valid casting
        direction = player.status.split('_')[0]
        if player.mana >= magic_data[player.spell]['cost']:
            player.mana -= magic_data[player.spell]['cost']
            self.sfx.play()
            self.image = pygame.image.load(full_path).convert_alpha()
            if direction == 'right':
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,10))
            elif direction == 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,10))
            elif direction == 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,10))
            elif direction == 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(10,-10))
            self.hitbox = self.rect
        else:
            self.image = pygame.image.load('./level_graphics/magic/fizzle.png')
            self.rect = self.image.get_rect(center = player.rect.center)
        
