#---to do---
# give keywords one key with a list as def? ('keywords':[Taunt, Reborn])
# make living constellation work (losing it give)

import gcfg
import combat
import cfg1
import cfg2
import turn
import copy

# type_list = []
# type_group_list = []
# for minion in gcfg.cfg.board:
#     type_group_list.append(minion['type'])

# print(type_group_list)

# # delete empty lists // append singular lists
# for type_group in type_group_list:
#     if len(type_group) == 0:
#         del type_group
#     elif len(type_group) == 1:
#         type_list.append(type_group)

# print(type_group_list)
# print(type_list)

# # try every possible combination...
# initial_type_list_length = copy.copy(len(type_list))

# type_list[initial_type_list_length + 1] = i1
# type_list[initial_type_list_length + 2] = i2

# print(type_group_list)
# print(type_list)

turn.create_pool()

game_going = True


# for each turn
while game_going == True:
    gcfg.turn += 1
    #for each player, set current player and play
    for player in gcfg.player_list:
        gcfg.cfg = __import__(player)
        turn.turn_input()
    #combat
    combat.combat()
    if gcfg.start_gold < 10:
        gcfg.start_gold += 1

