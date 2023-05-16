from unittest.mock import Mock, patch
from src.player import Player


@patch('src.player.pygame.image.load')
def test_sprite_update(mock_pygame):
    player_test = Player((0, 0), [], None)
    mock_pygame.assert_called_with('./level_graphics/characters/player/player-down.png')
    player_test.status = 'foo'
    player_test.sprite_update()
    mock_pygame.assert_called_with('./level_graphics/characters/player/player-foo.png')
    assert mock_pygame.call_count == 2
    