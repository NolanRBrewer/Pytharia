import pytest
from src.player import Player
import pygame


def test_keypresses():
    test_keys = key.copy()
    test_keys[pygame.K_w] = True
    player_test = Player((0, 0), [], None)
    player_test.input(test_keys)
    assert player_test.status == 'down'
    assert player_test.attacking == True


key = {pygame.K_w: False,
       pygame.K_UP: False,
       pygame.K_s: False,
       pygame.K_DOWN: False,
       pygame.K_a: False,
       pygame.K_LEFT: False,
       pygame.K_RIGHT: False,
       pygame.K_d: False,
       pygame.K_k: False}
