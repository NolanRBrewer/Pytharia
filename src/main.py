import pygame
import pygame.freetype
from pygame.sprite import Sprite
from settings import *
from level import Level
import sys
from enum import Enum

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    title_surface = pygame.image.load('./level_graphics/menu_graphics/Title_Screen_with_title.png').convert()
    title_rect = title_surface.get_rect(topleft=(0,0))
    screen.blit(title_surface, title_rect)
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level()

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    title_surface = pygame.image.load('./level_graphics/menu_graphics/Title_Screen_with_title.png').convert()
    title_rect = title_surface.get_rect(topleft=(0,0))


    start_btn = UIElement(
        center_position=((WIDTH / 4), (HEIGHT / 2)),
        font_size=30,
        bg_rgb=UI_BG_COLOR,
        text_rgb=UI_BORDER_COLOR_ACTIVE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=((WIDTH / 4), 500),
        font_size=30,
        bg_rgb=UI_BG_COLOR,
        text_rgb=UI_BORDER_COLOR_ACTIVE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(title_surface, title_rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def play_level():
    game = Game()
    game.run()

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1

class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Pytharia')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.level.toggle_upgrade_menu()
                    if event.key == pygame.K_q:
                        self.level.toggle_quest_menu()
                    if event.key == pygame.K_c:
                        self.level.toggle_control_menu()

            self.screen.fill(EDGE_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    main()