import pygame
from entity import Entity
from settings import *

class Enemy(Entity):
    def __init__(self,monster_name, pos, groups,obstacle_sprites, damage_player, add_exp):
        # general
        super().__init__(groups)
        self.sprite_type = 'enemy'
        # graphics setup
        self.image = pygame.image.load(f'./level_graphics/characters/enemies/{monster_name}.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        # status
        self.status  = 'idle'
        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # player interaction
        self.can_attack = True
        self.attack_time =  None
        self.attack_cd = 400
        self.damage_player = damage_player
        self.add_exp = add_exp
        
        # immunity timer
        self.vulnerable = True
        self.hit_time = None
        self.immunity_duration = 300


        # stats
        self.monster_name = monster_name
        monster_info = enemy_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.chase_radius = monster_info['chase_radius']
        self.attack_type = monster_info['attack_type']
        # sounds
        self.attack_sfx = pygame.mixer.Sound(monster_info['attack_sound'])
        self.attack_sfx.set_volume(0.2)
        self.hit_sound = pygame.mixer.Sound('audio/player_sfx/hit.wav')
        self.hit_sound.set_volume(0.2)
        self.death_sound = pygame.mixer.Sound('audio/enemy_attacks/death.wav')
        self.death_sound.set_volume(0.2)
    
    def detect_player(self,player):
        '''
        OBTAIN enemy and player vectors
        DETERMINE distance from player to enemy AND
        the direction the enemy will move in. 
        '''
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        # use magnitude to convert the difference of two vectors into a distance
        distance = (player_vector - enemy_vector).magnitude()
        # normalize the vector difference to determine the direction of movement. 
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
           direction =  pygame.math.Vector2()

        return (distance, direction)
    
    def get_status(self, player):
        '''
        by determining the distance and comparing it with each enemy's 
        chase radius and attack radius we update the enemy's behavior
        '''
        distance = self.detect_player(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
        elif distance <= self.chase_radius:
            self.status = 'chase'
        else:
            self.status = 'idle'

    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.attack_sfx.play()
            self.damage_player(self.attack_damage)
            self.can_attack = False
        elif self.status == 'chase':
            self.direction = self.detect_player(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.detect_player(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            elif attack_type == 'magic':
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.hit_sound.play()
            self.vulnerable = False
    
    def hit_recoil(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    
    def check_death(self):
        if self.health <= 0:
            self.death_sound.play()
            self.kill()
            self.add_exp(self.exp)

    def attack_cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cd:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.immunity_duration:
                self.vulnerable = True

    def update(self):
        self.hit_recoil()
        self.damage_animate()
        self.movement(self.speed)
        self.attack_cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)