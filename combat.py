import gcfg
import cfg1
import cfg2
import random
import copy
import abilities

gcfg.combat_board = []

#import boards
playernum = 0
for player in gcfg.player_list:
    gcfg.combat_board.append(copy.deepcopy(__import__(player).board))
    playernum += 1

#choose and define first attacking
attacking_player = random.choice([0, 1])
initial_attacking_player = attacking_player
defending_player = int(not bool(attacking_player))

winner = 'combat ongoing'
#attacking loop
done = False
attacking_slot = 0
while True:
    #check if all of one side is dead (at start in case one board is already empty)
    if gcfg.combat_board[0] == [] and gcfg.combat_board[1] == []:
        winner = 'Tie'
        damage = 0
        loser_health = None
        break
    elif gcfg.combat_board[1] == []:
        winner = 'Player 1'
        damage = cfg1.tav_tier
        for minion in gcfg.combat_board[0]:
            damage += minion['tier']
        cfg2.health -= damage
        loser_health = cfg2.health
        break
    elif gcfg.combat_board[0] == []:
        winner = 'Player 2'
        damage = cfg2.tav_tier
        for minion in gcfg.combat_board[1]:
            damage += minion['tier']
        cfg1.health -= damage
        loser_health = cfg1.health
        break
    else:
        #invert attacking player
        defending_player = int(attacking_player)
        attacking_player = int(not defending_player)
        print(f"Player 1's board is:{gcfg.combat_board[0]}")
        print(f"Player 2's board is:{gcfg.combat_board[1]}")

        # 0 attack check
        if gcfg.combat_board[attacking_player][attacking_slot]['attack'] == 0:
            for minion in gcfg.combat_board[attacking_player]:
                if gcfg.combat_board[attacking_player][attacking_slot]['attack'] == 0:
                    attacking_slot += 1
            if gcfg.combat_board[attacking_player][attacking_slot]['attack'] == 0:
                    defending_player = int(attacking_player)
                    attacking_player = int(not defending_player)
                    for minion in gcfg.combat_board[attacking_player]:
                        if gcfg.combat_board[attacking_player][attacking_slot]['attack'] == 0:
                            attacking_slot += 1
                    if gcfg.combat_board[attacking_player][attacking_slot]['attack'] == 0:
                        winner = 'Tie'
                        break
        
        
        
        
        # attack time
        abilities.events.attack(defending_player, attacking_player, attacking_slot)

        #set next minion to attack
        if attacking_player == initial_attacking_player:
            attacking_slot += 1

        #kill dead minions
        abilities.events.kill_dead_minions(attacking_slot)


print(f"Player 1's board is:{gcfg.combat_board[0]}")
print(f"Player 2's board is:{gcfg.combat_board[1]}")
print(f'Winner: {winner}')
if loser_health != None:
    print(f'The loser took {damage} damage, leaving them at {loser_health} health.')
