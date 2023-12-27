import pygame
from settings import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack,create_spell, end_attack):
        super().__init__(groups)
        # graphics setup
        self.image = pygame.image.load('./level_graphics/characters/player/down.png').convert_alpha()
        self.status = 'down'
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, HITBOX_OFFSET['player'])
         # Player Stats
        self.stats = {'health': 100,'magic': 100, 'attack': 10, 'wisdom': 4, 'speed': 4}
        self.max_stats = {'health': 300,'magic': 250, 'attack': 20,'wisdom': 10, 'speed': 8}
        self.upgrade_cost = {'health': 100,'magic': 100, 'attack': 100, 'wisdom': 100, 'speed': 100}
        self.health = self.stats['health']
        self.mana = self.stats['magic']
        self.speed = self.stats['speed']
        self.exp = 5000
        # attacking
        self.attacking = False
        self.attack_cd = 300
        self.attack_time = None
        # weapon
        self.create_attack = create_attack
        self.end_attack = end_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_change_weapon = True
        self.switch_time = None
        self.switch_cooldown = 200
        # magic
        self.create_spell = create_spell
        self.magic_index = 0
        self.spell = list(magic_data.keys())[self.magic_index]
        self.spell_potency = magic_data[self.spell]['potency']
        self.spell_cost = magic_data[self.spell]['cost']
        self.can_change_magic = True
        #sounds
        self.weapon_sound = pygame.mixer.Sound(weapon_data[self.weapon]['attack_sound'])
        self.weapon_sound.set_volume(0.2)
        # receiving damage
        self.vulnerable = True
        self.damage_time = None
        self.immunity_duration = 500
        # collison
        self.obstacle_sprites = obstacle_sprites
                
    def input(self, controls):
        if not self.attacking:
            # movement inputs
            # Up and down movement
            # Upward movement registers before downward. If both are presssed the player will move up.
            if controls[pygame.K_w] or controls[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif controls[pygame.K_s] or controls[pygame.K_DOWN]:
                self.direction.y = +1
                self.status = 'down'
            else:
                # if a key is not being pressed no movement
                self.direction.y = 0
            # left and right movement
            # right key activation registers before left. If both are pressed the player will move right.
            if controls[pygame.K_d] or controls[pygame.K_RIGHT]:
                self.direction.x = +1
                self.status = 'right'
            elif controls[pygame.K_a] or controls[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                # if no key is pressed no movement
                self.direction.x = 0
            #  attack input
            if controls[pygame.K_k]:
                self.attacking = True
                self.weapon_sound.play()
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            if controls[pygame.K_m]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_spell()
            
            # switch weapon
            if controls[pygame.K_0] and self.can_change_weapon:
                self.can_change_weapon = False
                self.switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                self.weapon_index = self.weapon_index % len(list(weapon_data.keys()))
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                self.weapon_sound = pygame.mixer.Sound(weapon_data[self.weapon]['attack_sound'])
            if controls[pygame.K_9] and self.can_change_weapon:
                self.can_change_weapon = False
                self.switch_time = pygame.time.get_ticks()
                self.weapon_index -= 1
                self.weapon_index = self.weapon_index % len(list(weapon_data.keys()))
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                self.weapon_sound = pygame.mixer.Sound(weapon_data[self.weapon]['attack_sound'])

            # switch magic
            if controls[pygame.K_p] and self.can_change_magic:
                self.can_change_magic = False
                self.switch_time = pygame.time.get_ticks()
                self.magic_index += 1
                self.magic_index = self.magic_index % len(list(magic_data.keys()))
                self.spell = list(magic_data.keys())[self.magic_index]
            if controls[pygame.K_o] and self.can_change_magic:
                self.can_change_magic = False
                self.switch_time = pygame.time.get_ticks()
                self.magic_index -= 1
                self.magic_index = self.magic_index % len(list(magic_data.keys()))
                self.spell = list(magic_data.keys())[self.magic_index]

    def sprite_update(self):
        self.image = pygame.image.load(f'./level_graphics/characters/player/{self.status}.png').convert_alpha()

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x, self.direction.y = 0,0
            if not 'attack' in self.status:
                if 'idle' in self. status:
                    # overwrite idle status
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status 
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cd + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.end_attack()
        
        if not self.can_change_weapon:
            if current_time - self.switch_time >= self.switch_cooldown:
                self.can_change_weapon = True
        
        if not self.can_change_magic:
            if current_time - self.switch_time >= self.switch_cooldown:
                self.can_change_magic = True
        
        if not self.vulnerable:
            if current_time - self.damage_time >= self.immunity_duration:
                self.vulnerable = True

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return  base_damage + weapon_damage

    def get_full_magic_damage(self):
        magic_damage = (magic_data[self.spell]['potency'] + (self.stats['wisdom'] * 1.25))
        return magic_damage

    def get_stat_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def mana_recovery(self):
        if self.mana < self.stats['magic']:
            self.mana += (0.01 * self.stats['wisdom']) 
        else:
            self.mana = self.stats['magic']

    def natural_regen(self):
        if self.health < self.stats['health']:
            self.health += 0.02
        else:
            self.health = self.stats['health']

    def update(self):
        # control calls
        keys = pygame.key.get_pressed()
        self.input(keys)
        # visuals
        self.sprite_update()
        self.damage_animate()
        # timers and statuses
        self.cooldowns()
        self.get_status() 
        # stat constants
        self.mana_recovery()
        self.natural_regen()
        # movement
        self.movement(self.stats['speed'])
