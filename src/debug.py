import pygame
pygame.init()
font = pygame.font.Font(None, 30)


def debug(info, y=10, x=10):
    diplay_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, 'white')
    debug_rect = debug_surface.get_rect(topleft=(x, y))
    pygame.draw.rect(diplay_surface, 'black', debug_rect)
    diplay_surface.blit(debug_surface, debug_rect)
