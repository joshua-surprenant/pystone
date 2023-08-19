#---to do---
# make scallywag work at all
# bug hunt (added like 1000 things and didnt test any of them sure i wont regret this)


import gcfg

import cfg1
import cfg2
import turn

turn.create_pool()

game_going = True


# for each turn
while game_going == True:
    #for each player, set current player and play
    for player in gcfg.player_list:
        gcfg.cfg = __import__(player)
        turn.turn_input()
    #combat
    import combat
    if gcfg.start_gold < 10:
        gcfg.start_gold += 1

