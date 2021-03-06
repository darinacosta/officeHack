import libtcodpy as libtcod
import shelve
import gameconfig
from interface.helpers import render_all, clear_console, message, message_box
from game.controls import handle_keys
from maps.mapconfig import make_map
from objects.classes import Fighter, Player, Object

def new_game():
    # create player
    player_component = Player(inventory=[])
    fighter_component = Fighter(hp=30, defense=1, power=5, xp=0)
    gameconfig.player = Object(0, 0, '@', 'Hero', libtcod.white, blocks=True, player=player_component, fighter=fighter_component)

    # creat level map
    make_map()

    # add first level to game_levels
    first_level = [ gameconfig.objects,
        gameconfig.level_map,
        gameconfig.stairs_up,
        gameconfig.stairs_down,
        gameconfig.color_theme,
        gameconfig.fov_map
    ]
    gameconfig.game_levels.append(first_level)

def save_game():
    # open new empty shelve - overwrites old
    file = shelve.open('savegame', 'n')
    file['map'] = gameconfig.level_map
    file['fov'] = gameconfig.fov_map
    file['objects'] = gameconfig.objects
    file['player'] = gameconfig.player
    file['game_msgs'] = gameconfig.game_msgs
    file['stairs_up'] = gameconfig.stairs_up
    file['stairs_down'] = gameconfig.stairs_down
    file['color_theme'] = gameconfig.color_theme
    file['game_level'] = gameconfig.game_level
    file['game_levels'] = gameconfig.game_levels
    file.close()

def load_game():
    # open previously saved shelve
    clear_console(gameconfig.con)
    file = shelve.open('savegame', 'r')
    gameconfig.level_map = file['map']
    gameconfig.fov_map = file['fov']
    gameconfig.objects = file['objects']
    gameconfig.player = file['player']
    gameconfig.game_msgs = file['game_msgs']
    gameconfig.stairs_up = file['stairs_up']
    gameconfig.stairs_down = file['stairs_down']
    gameconfig.color_theme = file['color_theme']
    gameconfig.game_level = file['game_level']
    gameconfig.game_levels = file['game_levels']
    file.close()

def play_game():
    game_state = 'playing'
    player_action = None
    fov_recompute = True

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,gameconfig.key,gameconfig.mouse)

        render_all(fov_recompute)
        player_action = handle_keys()

        if player_action == 'exit':
            save_game()
            break

        if player_action == 'stairs up':
            up_level()

        if player_action == 'stairs new':
            new_level()

        if player_action == 'stairs down':
            down_level()

        if game_state == 'playing' and player_action != 'no turn':
            fov_recompute = True
            for obj in gameconfig.objects:
                if obj.ai:
                    obj.ai.take_turn(gameconfig.fov_map, gameconfig.player)

def up_level():
    gameconfig.game_level -= 1
    golevel = gameconfig.game_level - 1
    gameconfig.objects = gameconfig.game_levels[golevel][0]
    gameconfig.level_map = gameconfig.game_levels[golevel][1]
    gameconfig.stairs_up = gameconfig.game_levels[golevel][2]
    gameconfig.stairs_down = gameconfig.game_levels[golevel][3]
    gameconfig.color_theme = gameconfig.game_levels[golevel][4]
    gameconfig.fov_map = gameconfig.game_levels[golevel][5]

    # player position
    gameconfig.player.x = gameconfig.stairs_down.x
    gameconfig.player.y = gameconfig.stairs_down.y
    clear_console(gameconfig.con)

def down_level():
    gameconfig.game_level += 1
    golevel = gameconfig.game_level - 1
    gameconfig.objects = gameconfig.game_levels[golevel][0]
    gameconfig.level_map = gameconfig.game_levels[golevel][1]
    gameconfig.stairs_up = gameconfig.game_levels[golevel][2]
    gameconfig.stairs_down = gameconfig.game_levels[golevel][3]
    gameconfig.color_theme = gameconfig.game_levels[golevel][4]
    gameconfig.fov_map = gameconfig.game_levels[golevel][5]

    # player position
    gameconfig.player.x = gameconfig.stairs_up.x
    gameconfig.player.y = gameconfig.stairs_up.y
    clear_console(gameconfig.con)

def new_level():
    # go to next level
    # we should also consider storing the previous levels so you can return to previously explored ones
    message('You take a moment to rest and recover your strength.', libtcod.light_cyan)
    gameconfig.player.fighter.heal(gameconfig.player.fighter.max_hp / 2)
    message('After a moment of peace, you descend deeper into the depths of horror.', libtcod.dark_red)
    gameconfig.game_level += 1

    # create new level
    clear_console(gameconfig.con)
    make_map()

    new_level = [ gameconfig.objects,
        gameconfig.level_map,
        gameconfig.stairs_up,
        gameconfig.stairs_down,
        gameconfig.color_theme,
        gameconfig.fov_map
    ]
    gameconfig.game_levels.append(new_level)
