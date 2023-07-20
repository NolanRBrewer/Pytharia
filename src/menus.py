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
                self.stat_windows[self.selection_index].trigger(self.player)
            
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
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        # title 
        title_surface = self.font.render(name, False, color)
        title_rect = title_surface.get_rect(midtop= self.rect.midtop + pygame.math.Vector2(0,20))
        # cost
        cost_surface = self.font.render(f'{int(cost)} EXP', False, color)
        cost_rect = cost_surface.get_rect(midbottom= self.rect.midbottom - pygame.math.Vector2(0,20))
        # draw
        surface.blit(title_surface,title_rect)
        surface.blit(cost_surface, cost_rect)

    def display_bar(self,surface,value,max_value, selected):
        # draw setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame. Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value/max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # draw bar
        pygame.draw.line(surface, color, top, bottom,5)
        pygame.draw.rect(surface, color, value_rect)
    
    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4
            if upgrade_attribute == 'health':
                player.health = player.stats['health']
            elif upgrade_attribute == 'magic':
                player.mana = player.stats['magic']
        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED if self.index == selection_num else UI_BG_COLOR, self.rect)
        pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED if self.index == UPGRADE_BORDER_COLOR_SELECTED else UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface,name,cost,self.index == selection_num)
        self.display_bar(surface,value,max_value,self.index == selection_num)

class ControlsMenu:
    def __init__(self):
        # general set up
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.section_titles = ['Movement','Actions','Credits']
        # self.section_images = [import_folder(''), import_folder(''), import_folder('')]
        # display dimensions
        self.height = self.display_surface.get_size()[1] * 0.25
        self.width = self.display_surface.get_size()[0] * 0.8
        self.create_control_window()
    
    def create_control_window(self):
        windows_number = 3
        self.control_windows = []
        for index, control_window in enumerate(range(windows_number)):
            # horizontal pos
            full_height = self.display_surface.get_size()[1]
            
            left = (control_window) + self.width * 0.125
            # vertical pos
            offset  = full_height * 0.05
            if index == 0:
                # draw from top for first box
                top = offset
            else:
                # calculate offset them draw box 
                increment = index / windows_number

                top = (full_height * increment) + offset

            # create box
            control_window = ControlsWindow(left,top,self.width,self.height, self.font)
            self.control_windows.append(control_window)
    
    def display(self): 
        
        for index, control_window in enumerate(self.control_windows):
            name = self.section_titles[index]
            # image = self.section_images[index]
            control_window.display(self.display_surface, name, index)

class ControlsWindow:
    def __init__(self,l,t,w,h,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.font = font

    def display_names(self, surface, name, index):
        # title 
        title_surface = self.font.render(name, False, TEXT_COLOR)
        title_rect = title_surface.get_rect(midtop= self.rect.midtop + pygame.math.Vector2(0,20))
        # draw
        surface.blit(title_surface,title_rect)
        self.control_images(surface, index)
        self.control_text(surface, index)
        

    def control_images(self, surface, index):
        if index == 0:
            width_offset = WIDTH * 0.12
            height_offset = 300
            menu_image = pygame.image.load('./level_graphics/menu_graphics/wasd.png')
            image_surface = menu_image
            image_rect = surface.get_rect(center=self.rect.center + pygame.math.Vector2(width_offset,height_offset))
            surface.blit(image_surface, image_rect)

        elif index == 1:
            width_offset = WIDTH * 0.12
            height_offset = 300
            menu_image = pygame.image.load('./level_graphics/menu_graphics/kmop90.png')
            control_image = pygame.image.load('./level_graphics/menu_graphics/qec.png')
            image_surface = menu_image
            image_rect = surface.get_rect(center=self.rect.center + pygame.math.Vector2(width_offset,height_offset))
            control_surface = control_image
            control_rect = surface.get_rect(center=self.rect.center + pygame.math.Vector2(WIDTH * .75,height_offset))
            surface.blit(image_surface, image_rect)
            surface.blit(control_surface, control_rect)
        elif index == 2:
            width_offset = WIDTH * 0.12
            height_offset = 300
            menu_image = pygame.image.load('./level_graphics/menu_graphics/thankyou.png')
            image_surface = menu_image
            image_rect = surface.get_rect(center=self.rect.center + pygame.math.Vector2(width_offset,height_offset))
            surface.blit(image_surface, image_rect)

    def control_text(self,surface,index):
        if index == 0:
            text = 'W : move up         S : move down'
            text2 = 'A : move left      D : move right'
            info_surface = self.font.render(text, False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center)
            surface.blit(info_surface, info_rect)
            info_surface = self.font.render(text2, False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center + pygame.math.Vector2(0,30))
            surface.blit(info_surface, info_rect)
        elif index == 1:
            texts = {
                'attack_magic' : 'K : Use weapon    M : Cast spell',
                'switch_weapons': '9 : Last weapon  0 : next weapon',
                'switch_magic': 'O : Last spell     P : next spell',
                'quest_menu': 'Q : Quest Menu',
                'control_menu': 'C : Controls menu',
                'upgrade_menu': 'E : Level up menu',
            }
            # attacks
            info_surface = self.font.render(texts['attack_magic'], False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center - pygame.math.Vector2(80,30))
            surface.blit(info_surface, info_rect)
            # switch weapons
            info_surface = self.font.render(texts['switch_weapons'], False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center - pygame.math.Vector2(80,0))
            surface.blit(info_surface, info_rect)
            # switch magic
            info_surface = self.font.render(texts['switch_magic'], False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center - pygame.math.Vector2(80,-30))
            surface.blit(info_surface, info_rect)
            # quest menu
            info_surface = self.font.render(texts['quest_menu'], False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center + pygame.math.Vector2(340,5))
            surface.blit(info_surface, info_rect)
            # control menu
            info_surface = self.font.render(texts['control_menu'], False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center + pygame.math.Vector2(340,30))
            surface.blit(info_surface, info_rect)
            # upgrade menu
            info_surface = self.font.render(texts['upgrade_menu'], False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center + pygame.math.Vector2(340,55))
            surface.blit(info_surface, info_rect)

        elif index == 2:
            # rendering for credits menu box
            text2 = 'Thank you to evereyone at Underdog Devs who made my'
            text3 = 'education journey possible.'
            
            info_surface = self.font.render(text2, False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center + pygame.math.Vector2(70,0))
            surface.blit(info_surface, info_rect)
            info_surface = self.font.render(text3, False, TEXT_COLOR)
            info_rect = info_surface.get_rect(center= self.rect.center + pygame.math.Vector2(60,30))
            surface.blit(info_surface, info_rect)

    def display(self, surface, name, index):
        pygame.draw.rect(surface,UI_BG_COLOR, self.rect)
        pygame.draw.rect(surface,UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface,name, index)
        
class QuestMenu:
    def __init__(self) -> None:
        # general set up
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        # quest titles
        self.quest_titles = ['Defeat Desert Python', 'Defeat Snow Python', 'Complete Pyforce']
        self.quest_info = ['Travel to the Southern Desert and vanquish the Desert Python', 'Search the North Mountain and slay the Snow Python', 'Return the the village after freeing the world of the Pythons']
        #  display box dimensions
        self.height = self.display_surface.get_size()[1] * 0.25
        self.width = self.display_surface.get_size()[0] * 0.8
        self.create_quest_window()
    
    def create_quest_window(self):
        windows_number = 3
        self.quest_windows = []
        for index, quest_window in enumerate(range(windows_number)):
            # horizontal pos
            full_height = self.display_surface.get_size()[1]
            
            left = quest_window + self.width * 0.125
            # vertical pos
            offset  = full_height * 0.05
            if index == 0:
                # draw from top for first box
                top = offset
            else:
                # calculate offset them draw box 
                increment = index / windows_number

                top = (full_height * increment) + offset

            # create box
            quest_window = QuestWindow(left,top,self.width,self.height, self.font)
            self.quest_windows.append(quest_window)
    
    def display(self): 
        
        for index, quest_window in enumerate(self.quest_windows):
            name = self.quest_titles[index]
            objective = self.quest_info[index]
            # image = self.section_images[index]
            quest_window.display(self.display_surface, name, objective)

class QuestWindow:
    def __init__(self,l,t,w,h,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.font = font
        self.quest_image = pygame.image.load('./level_graphics/menu_graphics/quest-scroll.png')
    
    def display_quest(self, surface, name, objective):
        color = TEXT_COLOR
        # title 
        title_surface = self.font.render(name, False, color)
        title_rect = title_surface.get_rect(midtop= self.rect.midtop + pygame.math.Vector2(0,20))
        # info 
        info_surface = self.font.render(f'Objective: {str(objective)}', False, color)
        info_rect = info_surface.get_rect(center= self.rect.center)
        # image display
        width_offset = WIDTH * 0.12
        height_offset = 280
        image_surface = self.quest_image
        image_rect = surface.get_rect(center=self.rect.center + pygame.math.Vector2(width_offset,height_offset))

        # draw
        surface.blit(title_surface,title_rect)
        surface.blit(image_surface, image_rect)
        surface.blit(info_surface, info_rect)

    def display(self, surface, name, objective):
        pygame.draw.rect(surface,UI_BG_COLOR, self.rect)
        pygame.draw.rect(surface,UI_BORDER_COLOR, self.rect, 4)
        self.display_quest(surface, name, objective)

class TitleScreen:
    def __init__(self):
        # general set up
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.section_titles = ['Movement','Actions','Credits']
        # self.section_images = [import_folder(''), import_folder(''), import_folder('')]
        # display dimensions
        self.height = self.display_surface.get_size()[1] * 0.25
        self.width = self.display_surface.get_size()[0] * 0.8
        self.create_control_window()
    
    def create_control_window(self):
        windows_number = 3
        self.control_windows = []
        for index, control_window in enumerate(range(windows_number)):
            # horizontal pos
            full_height = self.display_surface.get_size()[1]
            
            left = (control_window) + self.width * 0.125
            # vertical pos
            offset  = full_height * 0.05
            if index == 0:
                # draw from top for first box
                top = offset
            else:
                # calculate offset them draw box 
                increment = index / windows_number

                top = (full_height * increment) + offset

            # create box
            control_window = ControlsWindow(left,top,self.width,self.height, self.font)
            self.control_windows.append(control_window)
    
    def display(self): 
        
        for index, control_window in enumerate(self.control_windows):
            name = self.section_titles[index]
            # image = self.section_images[index]
            control_window.display(self.display_surface, name, index)

class TitleScreen: 
        def __init__(self,l,t,w,h,font):
            self.rect = pygame.Rect(l,t,w,h)
            self.font = font
            self.quest_image = pygame.image.load('./level_graphics/menu_graphics/quest-scroll.png')
        
        def display_quest(self, surface, name, objective):
            color = TEXT_COLOR
            # title 
            title_surface = self.font.render(name, False, color)
            title_rect = title_surface.get_rect(midtop= self.rect.midtop + pygame.math.Vector2(0,20))
            # info 
            info_surface = self.font.render(f'Objective: {str(objective)}', False, color)
            info_rect = info_surface.get_rect(center= self.rect.center)
            # image display
            width_offset = WIDTH * 0.12
            height_offset = 280
            image_surface = self.quest_image
            image_rect = surface.get_rect(center=self.rect.center + pygame.math.Vector2(width_offset,height_offset))

            # draw
            surface.blit(title_surface,title_rect)
            surface.blit(image_surface, image_rect)
            surface.blit(info_surface, info_rect)

        def display(self, surface, name, objective):
            pygame.draw.rect(surface,UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR, self.rect, 4)
            self.display_quest(surface, name, objective)

