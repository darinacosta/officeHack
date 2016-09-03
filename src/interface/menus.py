import libtcodpy as libtcod
import gameconfig
import time
import textwrap
from interface.cli import cli_window
from interface.rendering import message
from objects.actions import read_write_file, random_object, remote_view

def highlight_selection(window, bgnd_color, sel_color, selected, width, height, header_height, x, y):
    libtcod.console_set_default_background(window, bgnd_color)
    libtcod.console_rect(window, 0, 0, width, height, False, libtcod.BKGND_SET)
    libtcod.console_set_default_background(window, sel_color)
    libtcod.console_rect(window, 0, selected+header_height, width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)
    libtcod.console_flush()

def menu(header, options, width=gameconfig.MENU_WIDTH, bgnd_color=None, fgnd_color=None, sel_color=None):
    # general selection menu
    # color inits
    if bgnd_color is None: bgnd_color = gameconfig.MENU_BKGND
    if fgnd_color is None: fgnd_color = libtcod.white
    if sel_color is None: sel_color = gameconfig.MENU_SELECT_BKGND

    if len(options) > 26: raise ValueError('Cannot have a MENU with more than 26 OPTIONS!')

    # calculate total height for the header (after auto-wrap) and one line per option
    header += '\n\n'
    header_height = libtcod.console_get_height_rect(gameconfig.con, 0, 0, width, gameconfig.SCREEN_HEIGHT, header)
    if header == '\n\n':
        header_height = 1
    height = len(options) + header_height + 1

    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
    libtcod.console_set_default_background(window, bgnd_color)
    libtcod.console_rect(window, 0, 0, width, height, False, libtcod.BKGND_SCREEN)

    #print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, fgnd_color)
    libtcod.console_print_rect_ex(window, 1, 1, width-2, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 1, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    #blit window contents
    x = gameconfig.SCREEN_WIDTH/2 - width/2
    y = gameconfig.SCREEN_HEIGHT/2 - height/2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)

    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    selected = 0
    while True:
        key = libtcod.console_wait_for_keypress(True)

        if options: # selection loop
            if key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_UP:
                if key.vk == libtcod.KEY_DOWN:
                    if selected < len(options):
                        selected += 1
                    else:
                        selected = 1
                if key.vk == libtcod.KEY_UP:
                    if selected > 1:
                        selected -= 1
                    else:
                        selected = len(options)

                # hightlight selected option
                highlight_selection(window, bgnd_color, sel_color, selected-1, width, height, header_height, x, y)

            if key.vk == libtcod.KEY_ENTER:
                if selected == 0:
                    selected = 1
                highlight_selection(window, bgnd_color, sel_color, selected-1, width, height, header_height, x, y)
                time.sleep(0.1)
                return(selected-1)

            # convert ascii to index
            index = key.c - ord('a')
            if index >= 0 and index < len(options):
                selected = index
                # hightlight selected option
                highlight_selection(window, bgnd_color, sel_color, selected, width, height, header_height, x, y)
                time.sleep(0.1)
                return index

        if key.vk == libtcod.KEY_ESCAPE:
            return None

def message_box(text, width=gameconfig.MENU_WIDTH):
    # popup message box
    menu(text, [], width)

def main_menu():
    # start game menu - logic handled in officehack.py

    #background image for menu
    img = libtcod.image_load('data/img/bg.png')
    libtcod.image_blit_2x(img, 0, 0, 0)

    # title
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_set_default_background(0, libtcod.flame)
    libtcod.console_print_ex(0, gameconfig.SCREEN_WIDTH/2, gameconfig.SCREEN_HEIGHT/2-4, libtcod.BKGND_SET, libtcod.CENTER,
        gameconfig.GAME_TITLE)
    libtcod.console_print_ex(0, gameconfig.SCREEN_WIDTH/2, gameconfig.SCREEN_HEIGHT/2-3, libtcod.BKGND_SET, libtcod.CENTER,
        gameconfig.GAME_AUTHOR)

    return menu('', ['New Game', 'Continue', 'Quit'], gameconfig.MAIN_MENU_WIDTH)

def inventory_menu(header, inventory):
    # inventory menu
    if len(inventory) == 0:
        options = ['Inventory is empty']
    else:
        options = []
        for item in inventory:
            options.append(item.inv_id + ' [' + str(item.count) +']')
    index = menu(header, options)
    if index is None or len(inventory) == 0: return None
    return inventory[index].item

def terminal(header=''):
    # computer terminal
    gameconfig.player_at_computer = True
    header = 'Welcome to TERMINAL-A' # give it a name eventually
    options = ['read_', 'write_', 'save_', 'remote_']
    index = menu(header, options, bgnd_color=libtcod.dark_azure,
        fgnd_color=libtcod.lighter_sky, sel_color=libtcod.light_azure)
    if options[index] == 'read_':
        floppy = None
        for item in gameconfig.player.player.inventory:
            if item.inv_id == 'floppy disc':
                floppy = item
                break
        if floppy is not None:
            floppy.item.use()
            cli_window(floppy.item.special)
    if options[index] == 'write_':
        cli_window()
    if options[index] == 'remote_':
        target = random_object()
        message('remote viewing' + target.name)
        remote_view(target)
        
    gameconfig.player_at_computer = False

def conversation(header, npc_name):
    # basic test conversation

    # messy portrait bullshit
    img = libtcod.image_load('data/img/portrait2x.png') # this should ultimately be an attribute the object posesses.
    portrait = libtcod.console_new(50, 20)
    libtcod.console_set_default_background(portrait, gameconfig.MENU_BKGND)
    libtcod.console_set_default_foreground(portrait, libtcod.white)
    libtcod.console_rect(portrait, 0, 0, 50, 20, False, libtcod.BKGND_SET)
    libtcod.console_print_ex(portrait, 10, 10, libtcod.BKGND_NONE, libtcod.LEFT, npc_name)
    #libtcod.image_blit_rect(img, portrait, 1, 1, -1, -1, libtcod.BKGND_SET) #1x size 8x10
    libtcod.image_blit_2x(img, portrait, 1, 1, 0, 0, -1, -1) #2x size 16x20
    libtcod.console_blit(portrait, 0, 0, 50, 20, 0, gameconfig.SCREEN_WIDTH/2-25, gameconfig.SCREEN_HEIGHT/2-16, 1.0, 1.0)

    responses = ['yeah.', 'I guess.', 'sure do.', 'maybe?', 'no way.']
    index = menu(header, responses)
    if index is None or len(responses) == 0: return None
    return responses[index]
