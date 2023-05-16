import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_numbers = len(player.stats)
        self.attribute_name = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font. Font(UI_FONT, UI_FONT_SIZE)
        # stat box dimensions
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_stats_windows()
        #  selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        controls = pygame.key.get_pressed()
        # choosing what item to upgrade right and left control
        if self.can_move:
            if controls[pygame.K_d] and self.selection_index < self.attribute_numbers - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif controls[pygame.K_a] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            # selection button
            if controls[pygame.K_m]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            
    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_stats_windows(self):
        self.stat_windows = []
        for index, stat_window in enumerate(range(self.attribute_numbers)):
            # horizontal pos
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_numbers
            left = (stat_window * increment) + (increment - self.width) // 2 
            # vertical pos
            
            top = self.display_surface.get_size()[1] * 0.1

            # create box
            stat_window = StatsWindow(left,top,self.width,self.height,index, self.font)
            self.stat_windows.append(stat_window)
            
    def display(self):
        self.input()
        self.selection_cooldown()
        
        for index, stat_window in enumerate(self.stat_windows):
            # get attributes from player 
            name = self.attribute_name[index]
            value = self.player.get_stat_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            stat_window.display(self.display_surface,self.selection_index,name, value, max_value, cost)

class StatsWindow:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        # title 
        title_surface = self.font.render(name, False, TEXT_COLOR)
        title_rect = title_surface.get_rect(midtop= self.rect.midtop + pygame.math.Vector2(0,20))
        # cost
        cost_surface = self.font.render(f'{int(cost)}', False, TEXT_COLOR)
        cost_rect = cost_surface.get_rect(midbottom= self.rect.midbottom - pygame.math.Vector2(0,20))
        # draw
        surface.blit(title_surface,title_rect)
        surface.blit(cost_surface, cost_rect)

    def display(self, surface, selection_num, name, value, max_value, cost):
    
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.display_names(surface,name,cost,False)