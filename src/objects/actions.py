import libtcodpy as libtcod
import gameconfig
from interface.helpers import message

def send_to_back(target, objects):
    #gotta get objects here somehow
    objects.remove(target)
    objects.insert(0, target_npc)

def player_death(player):
    # you ded
    message('You died!', libtcod.white)
    player.char = '%'
    player.color = libtcod.dark_red
    return 'dead' #game_state

def npc_death(npc):
    # npc death
    message(npc.name.capitalize() + ' is dead! You gain ' + str(npc.fighter.xp) + 'XP!', libtcod.cyan)
    npc.char = '%'
    npc.color = libtcod.dark_red
    npc.blocks = False
    npc.fighter = None
    npc.ai = None
    npc.name = 'remains of ' + npc.name
    npc.send_to_back(npc, objects) #gotta get objects here or take send_to_back call outside npc_death

def closest_npc(max_range):
    # find closest enemy to max range and in FOV
    closest_npc = None
    closest_dist = max_range + 1

    for obj in objects:
        if obj.fighter and not obj == player and libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
            dist = player.distance_to(obj)
            if dist < closest_dist:
                closest_npc = obj
                closest_dist = dist
    return closest_npc

def cast_heal(target):
    #heal the player
    if target.hp == target.max_hp:
	    message('You are already at full health.', libtcod.red)
	    return('cancelled')
    message('your wounds feel better.', libtcod.light_violet)
    target.heal(HEAL_AMOUNT)

def cast_lightning():
    #find nearest enemy and shock them with your deviant behaviour
    npc = closest_npc(LIGHTNING_RANGE)
    if npc is None:
        message('No enemy is close enough to be shocked by you.', libtcod.red)
        return 'cancelled'
    message('A lightning bold strikes the ' + npc.name + ', ZAP! For ' + str(LIGHTNING_DAMAGE) + ' damage.', libtcod.light_blue)
    npc.fighter.take_damage(LIGHTNING_DAMAGE)

def cast_fireball():
    message('Left-click a target tile, right-click to cancel.', libtcod.light_cyan)
    (x, y) = target_tile()
    if x is None: return 'cancelled'
    message('The fireball explodes burning everything in range.', libtcod.orange)

    for obj in objects:
        #damage everything in radius
        if obj.distance(x, y) <= FIREBALL_RADIUS and obj.fighter:
            message('The ' + obj.name + ' gets burned for ' + str(FIREBALL_DAMAGE) + ' hp.', libtcod.orange)
            obj.fighter.take_damage(FIREBALL_DAMAGE)

def cast_confusion():
    message('left-click an enemy to confuse. Right-click to cancel.', libtcod.light_cyan)
    npc = target_npc(CONFUSE_RANGE)
    if npc is None: return 'cancelled'
    old_ai = npc.ai
    npc.ai = Confusednpc(old_ai)
    npc.ai.owner = npc
    message('The ' + npc.owner.name + ' feels very confused', libtcod.light_green)
