import pygame

from trosnoth.const import (
    ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY, ACTION_EMOTE,
)
from trosnoth.gui.keyboard import VirtualKeySet, mouseButton

# Define virtual keys and their default bindings.
default_game_keys = VirtualKeySet((
    # Movement keys.
    ('left', pygame.K_a),
    ('down', pygame.K_s),
    ('right', pygame.K_d),
    ('jump', pygame.K_w),
    ('hook', mouseButton(3)),
    (ACTION_SHOW_TRAJECTORY, pygame.K_LSHIFT),
    (ACTION_DEBUGKEY, mouseButton(2)),

    # Used in replay mode.
    ('follow', pygame.K_EQUALS),

    # Menu keys.
    ('menu', pygame.K_ESCAPE),

    ('select upgrade', pygame.K_b),
    ('activate upgrade', pygame.K_SPACE),
    ('change nickname', pygame.K_F12),
    ('more actions', pygame.K_v),
    ('respawn', pygame.K_r),
    ('ready', pygame.K_y),
    (ACTION_EMOTE, pygame.K_t),

    ('no upgrade', pygame.K_0),

    ('chat', pygame.K_RETURN),
    ('leaderboard', pygame.K_p),
    ('toggle interface', pygame.K_DELETE),
    ('pause', pygame.K_PAUSE),

    ('toggle terminal', pygame.K_SCROLLOCK),
))

from trosnoth.model.upgrades import allUpgrades

for upgradeClass in allUpgrades:
    if upgradeClass.defaultPygameKey is not None:
        default_game_keys[upgradeClass.action] = upgradeClass.defaultPygameKey
del upgradeClass
