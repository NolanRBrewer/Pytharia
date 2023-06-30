import pygame
from settings import *
from tiles import *
from player import Player
from enemy import Enemy
from support import *
from debug import debug
from ui import UI
from attack import *
from magic import *
from menus import *


class Level:
    def __init__(self):
        # get display for the surface
        self.display_surface = pygame.display.get_surface()
        
        # sprite groupings
        self.visible_sprites = YCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.current_spell = None
        
        # set up sprites
        self.create_map()

        # display UI
        self.ui = UI()
        self.game_paused = False
        self.quest_display = False
        self.control_display = True
        self.upgrade_menu = Upgrade(self.player)
        self.control_menu =  ControlsMenu()
        self.quest_menu = QuestMenu()

    def create_map(self):
        # forming the world by creating obstacles on top of an image
        # 
        layouts = {
            'boundary': import_csv_layout('./level_graphics/map/map_boundaries.csv'),
            'bushes': import_csv_layout('./level_graphics/map/map_bushes.csv'),
            'objects': import_csv_layout('./level_graphics/map/map_objects.csv'),
            'entities': import_csv_layout('./level_graphics/map/map_entities.csv')
        }
        # storing all graphics by type
        graphics = {
            'bushes': import_folder('./level_graphics/environment/bush/bush.png'),
            '13': import_folder('./level_graphics/environment/objects/tree.png'),
            '12': import_folder('./level_graphics/environment/objects/snow-tree.png'),
            '1': import_folder('./level_graphics/environment/objects/large-rock.png'),
            '0': import_folder('./level_graphics/environment/objects/desert-rock.png'),
            '2': import_folder('./level_graphics/environment/objects/snow-rock.png')
        }

        for style, layout in layouts.items():
            # selecting the csv
            for row_index, row in enumerate(layout):
                for col_index, voxel in enumerate(row):
                    if voxel != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y),
                                 self.obstacle_sprites, 'invisible')
                        
                        if style == 'bushes':
                            # create bush
                            bush_image = graphics['bushes']
                            Tile((x, y), [self.visible_sprites,
                                          self.obstacle_sprites, 
                                          self.attackable_sprites], 
                                          'bush', bush_image)
                            
                        if style == 'objects':
                            # create object
                            object_image = graphics[str(voxel)]
                            Tile((x, y), [self.visible_sprites,
                                    self.obstacle_sprites, 
                                    self.attackable_sprites], 
                                    'objects', object_image)

                        
                        if style == 'entities':
                            if voxel == '12': 
                                self.player = Player((x, y), 
                                            [self.visible_sprites],
                                            self.obstacle_sprites, 
                                            self.create_attack, 
                                            self.create_spell, 
                                            self.end_attack)
                            else:
                                if voxel == '5': monster_name = 'snow_python'
                                elif voxel == '0': monster_name = 'desert_slime'
                                elif voxel == '4': monster_name = 'desert_python'
                                else: monster_name = 'field_slime'
                                Enemy(monster_name, (x, y), [self.visible_sprites,
                                                             self.attackable_sprites],
                                                             self.obstacle_sprites,
                                                             self.damage_player,
                                                             self.add_exp)
                                
    def create_attack(self):
        self.current_attack = Weapon(self.player, 
                                     [self.visible_sprites,
                                     self.attack_sprites])
    
    def create_spell(self):
        if self.player.spell == 'heal':
            self.current_spell = Heal(self.player,[self.visible_sprites])
        if self.player.spell == 'barrier':
            self.create_spell = Barrier(self.player,[self.visible_sprites, self. obstacle_sprites, self.attackable_sprites])
        if self.player.spell == 'bubble':
            self.current_spell = Bubble(self.player,[self.visible_sprites, self.attack_sprites])
        if self.player.spell == 'snowfall':
            self.current_spell = Snowfall(self.player,[self.visible_sprites, self.attack_sprites])
        if self.player.spell == 'flame':
            self.current_spell = Flame(self.player,[self.visible_sprites, self.attack_sprites])

    def end_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None
        if self.current_spell:
            self.current_spell.kill()
            self.current_spell = None
    
    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.damage_time = pygame.time.get_ticks()

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target in collision_sprites:
                        if target.sprite_type == 'bush':
                            target.kill()
                        elif target.sprite_type == 'objects':
                            pass
                        else:
                            target.get_damage (self.player, attack_sprite.sprite_type)

    def add_exp(self, exp_amount):
        self.player.exp += exp_amount
    
    def toggle_upgrade_menu(self):
        self.game_paused = not self.game_paused

    def toggle_quest_menu(self):
        self.quest_display = not self.quest_display

    def toggle_control_menu(self):
        self.control_display = not self.control_display

    def run(self):
        # update and draw the level the player is on
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            # other menus close
            self.quest_display = False
            # display upgrade menu 
            self.upgrade_menu.display()
        elif self.control_display:
            self.game_paused = False
            self.quest_display = False
            # display control menu
            self.control_menu.display()
        elif self.quest_display:
            self.game_paused = False
            self.control_display = False
            # display quest menu
            self.quest_menu.display()
        
        else:
            # Run game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            
class YCameraGroup(pygame.sprite.Group):
    '''
    Creating a sprite overlap to emulate a sense of depth. 
    i.e. a character sprite looks as if it is standing behind an obstacle or other character.
    '''

    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_screen_width = self.display_surface.get_size()[0] // 2
        self.half_screen_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(
            self.half_screen_width, self.half_screen_height)

        # creating the floor
        self.floor_surf = pygame.image.load(
            './level_graphics/map/basic-map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # Creating the offset
        self.offset.x = player.rect.centerx - self.half_screen_width
        self.offset.y = player.rect.centery - self.half_screen_height

        # drawing floor and offset
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites()if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)