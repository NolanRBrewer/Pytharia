WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player':-26,
    'objects': -40,
    'bushes':-10,
    'invisible':0
}

# UI
# HEALTH
HEALTH_BAR_HEIGHT = 25
HEALTH_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
# MAGIC
MAGIC_BAR_HEIGHT = 20
MAGIC_BAR_WIDTH = 150
UI_FONT = './fonts/PixelCombat.ttf'
UI_FONT_SIZE = 18
# UI COLOR
UI_BG_COLOR = '#1e003d'
UI_BORDER_COLOR = '#222222'
TEXT_COLOR = '#ffffff'
ITEM_BOX_COLOR = '#111111'
# STATS COLORS
HEALTH_COLOR = '#FA4587'
MAGIC_COLOR = '#D226E6'
UI_BORDER_COLOR_ACTIVE = '#C6b725'
# UPGRADE MENU COLORS
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
UPGRADE_BORDER_COLOR_SELECTED = '#1e003d'
# TITLE SCREEN COLORS
TITLE_SCREEN_BG_COLOR = '000000'
# MISC COLORS
EDGE_COLOR = '#639BFF'

# Weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 20, 'graphic': './level_graphics/weapons/sword/full.png', 'attack_sound': 'audio/player_sfx/sword.wav'},
    'dagger': {'cooldown': 75, 'damage': 10, 'graphic': './level_graphics/weapons/dagger/full.png', 'attack_sound': 'audio/enemy_attacks/slash.wav'},
    'battleaxe': {'cooldown': 200, 'damage': 45, 'graphic': './level_graphics/weapons/battleaxe/full.png', 'attack_sound': 'audio/player_sfx/battleaxe.wav'}
}
# Magic
magic_data = {
    'flame': {'cooldown': 100, 'potency': 20,'cost': 15, 'graphic': './level_graphics/magic/flame.png', 'attack_sound': 'audio/player_sfx/fire.wav'},
    'bubble': {'cooldown': 100, 'potency': 10, 'cost': 10 , 'graphic': './level_graphics/magic/bubble.png', 'attack_sound': 'audio/player_sfx/hit.wav'},
    'snowfall': {'cooldown': 100, 'potency': 20, 'cost': 20 , 'graphic': './level_graphics/magic/snowfall.png', 'attack_sound': 'audio/player_sfx/battleaxe.wav'},
    'barrier': {'cooldown': 100, 'potency': 0, 'cost': 10 , 'graphic': './level_graphics/magic/barrier.png', 'attack_sound': 'audio/player_sfx/magic_barrier.wav'},
    'heal': {'cooldown': 100, 'potency': 25, 'cost': 20, 'graphic': './level_graphics/magic/heal.png', 'attack_sound': 'audio/player_sfx/heal.wav'}
}
# Enemies
enemy_data = {
    'field_slime': {'health': 100, 'exp': 100, 'damage': 20, 'speed': 2, 'resistance': 4, 'attack_radius': 60, 'chase_radius': 300,'attack_type': 'slash', 'graphic': './level_graphics/characters/enemies/field_slime.png', 'attack_sound':'audio/enemy_attacks/slash.wav'},
    'desert_slime': {'health': 100, 'exp': 100, 'damage': 30, 'speed': 2, 'resistance': 4, 'attack_radius': 70, 'chase_radius': 280, 'attack_type': 'slash', 'graphic': './level_graphics/characters/enemies/desert_slime.png', 'attack_sound':'audio/enemy_attacks/slash.wav'},
    'desert_python': {'health': 300, 'exp': 250, 'damage': 50, 'speed': 3, 'resistance': 5, 'attack_radius': 70, 'chase_radius': 360,'attack_type': 'claw', 'graphic': './level_graphics/characters/enemies/desert_python.png', 'attack_sound':'audio/enemy_attacks/claw.wav'},
    'snow_python': {'health': 300, 'exp': 250, 'damage': 600, 'speed': 3, 'resistance': 5, 'attack_radius': 70, 'chase_radius': 360,'attack_type': 'claw', 'graphic': './level_graphics/characters/enemies/snow_python.png', 'attack_sound':'audio/enemy_attacks/claw.wav'}
}