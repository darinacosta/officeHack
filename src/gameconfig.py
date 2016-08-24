import libtcodpy as libtcod

GAME_STATE = 'playing'
ACTIVE_OBJECTS = []

GAME_MSGS = []
MOUSE = libtcod.Mouse()
KEY = libtcod.Key()

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

INVENTORY_WIDTH = 50

HEAL_AMOUNT = 4

MAP_WIDTH = 80
MAP_HEIGHT = 43

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

MAX_ROOM_MONSTERS = 3
MAX_ROOM_ITEMS = 2

FOV_MAP = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
FOV_ALGO = 2
FOV_RECOMPUTE = True

FOV_LIGHT_WALLS = True
TORCH_RADIUS = 8

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 100)
color_light_ground = libtcod.Color(200, 180, 50)
