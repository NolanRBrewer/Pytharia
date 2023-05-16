import pygame
from settings import *
'''
The player statistics:
    Player health, attack, magic and speed

display the current health in proportion to max health
(and magic/ stamina if implemented)
'''
class UI:
    def  __init__(self):
        #   general 
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 20, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
        self.magic_bar_rect = pygame.Rect(10, 50, MAGIC_BAR_WIDTH, MAGIC_BAR_HEIGHT)
        # convert weapon dict
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        self.magic_graphics = []
        for spell in magic_data.values():
            path = spell['graphic']
            spell = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(spell)

    def show_meter(self, current, max_amount, bg_rect, color, vulnerable):
        #draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect,)
        # convert stats to pixels
        ratio = int(current) / int(max_amount)
        current_width = bg_rect.width * ratio 
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        #Draw the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        if not vulnerable:
           pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3) 

    def show_exp(self, exp):
       text_surf = self.font.render(str(int(exp)),False, TEXT_COLOR)
       text_rect = text_surf.get_rect(bottomright= ( 54, 105))
       pygame.draw.rect(self.display_surface,UI_BG_COLOR, text_rect.inflate(20,20))
       self.display_surface.blit(text_surf, text_rect)
       pygame.draw.rect(self.display_surface,UI_BORDER_COLOR, text_rect.inflate(20,20), 3 )
    
    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left,top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, ITEM_BOX_COLOR, bg_rect)
        if not has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 4)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect
    
    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 600, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center= bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 620, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center= bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)
    
    def display(self,player):
        self.show_meter(player.health, player.stats['health'],self.health_bar_rect, HEALTH_COLOR, player.vulnerable)
        self.show_meter(player.mana, player.stats['magic'],self.magic_bar_rect, MAGIC_COLOR, True)
        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, player.can_change_weapon)
        self.magic_overlay(player.magic_index, player.can_change_magic)
        
    
    