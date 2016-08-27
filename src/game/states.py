import libtcodpy as libtcod
import shelve
import gameconfig
from interface.interfaceconfig import initialize_controls
from interface.helpers import render_all
from game.controls import handle_keys
from maps.mapconfig import make_map, initialize_fov
from objects.classes import Fighter, Object

def new_game():
    # controls - setup key and mouse
    key, mouse = initialize_controls()

    # player - create player
    inventory = []
    #player_component = Player(inventory=inventory)
    fighter_component = Fighter(hp=30, defense=1, power=5, xp=0)
    player = Object(0, 0, '@', 'Hero', libtcod.white, blocks=True, fighter=fighter_component)
    player.level = 1

    # level
    objects, level_map, stairs = make_map(player)
    #dungeon_level = 1
    #get_leveldata() #bunch of stuff from here for HUD - currently disabled

    # fov
    fov_map, fov_recompute = initialize_fov(level_map)

    return key, mouse, inventory, player, objects, level_map, stairs, fov_map, fov_recompute

def save_game():
    # open new empty shelve - overwrites old
    file = shelve.open('savegame', 'n')
    file['map'] = level_map
    file['objects'] = objects
    file['player_index'] = objects.index(player)
    file['inventory'] = inventory
    file['game_msgs'] = game_msgs
    file['game_state'] = game_state
    file['stairs_index'] = objects.index(stairs)
    file['dungron_level'] = dungeon_level
    file.close()

"""def load_game():
    global level_map, objects, player, inventory, game_msgs, game_state, stairs, dungeon_level
    # open previously saved shelve
    file = shelve.open('savegame', 'r')
    level_map = file['map']
    objects = file['objects']
    player = objects[file['player_index']]
    inventory = file['inventory']
    game_msgs = file['game_msgs']
    game_state = file['game_state']
    stairs = objects[file['stairs_index']]
    dungeon_level = file['dungeon_level']
    file.close()
    # render FOV
    initialize_fov()"""

def play_game(player, objects, level_map, fov_map, key, mouse, con, panel):
    game_state = 'playing'
    player_action = None
    fov_recomputer = True

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
        
        render_all(player, objects, level_map, fov_map, con, panel)

        player_action = handle_keys(player, objects, level_map, key, mouse)
        if player_action == 'exit':
            save_game()
            break
        if game_state == 'playing' and player_action != 'no turn':
            for obj in objects:
                if obj.ai:
                    obj.ai.take_turn(fov_map, player)

"""def next_level():
    global dungeon_level

    # go to next level
    message('You take a moment to rest and recover your strength.', libtcod.light_cyan)
    player.fighter.heal(player.fighter.max_hp / 2)
    message('After a moment of peace, you descend deeper into the depths of horror.', libtcod.dark_red)
    dungeon_level += 1

    # create new level
    make_map()
    initialize_leveldata()
    initialize_fov()"""
