import gcfg
import random
cfg = gcfg.cfg
import itertools
import cfg1
import cfg2
import abilities

#pool creation
def create_pool():
    for minion in abilities.minion_list:
        total_pool_size = 0
        if minion['tier'] == 1:
            total_pool_size += 18
        if minion['tier'] == 2:
            total_pool_size += 15
        if minion['tier'] == 3:
            total_pool_size += 13
        if minion['tier'] == 4:
            total_pool_size += 11
        if minion['tier'] == 5:
            total_pool_size += 9
        if minion['tier'] == 6:
            total_pool_size += 6
        i=0
        while i<total_pool_size:
            gcfg.pool[minion['tier']-1].append(minion)
            i+=1

#shop refresh
def refresh_shop(slots=gcfg.cfg.shop_slots):
    cfg = gcfg.cfg
    if gcfg.cfg.current_shop != []:
        for card in gcfg.cfg.current_shop:
            gcfg.pool[card['tier']-1].append(card)
        cfg.current_shop = []
    i=0
    populating = 0
    current_tier_pool = []
    for tier in gcfg.pool:
        if gcfg.pool.index(tier) < gcfg.cfg.tav_tier:
            for card in tier:
                current_tier_pool.append(card)
    while populating < cfg.shop_slots:
        populating_card = current_tier_pool.pop(current_tier_pool.index(random.choice(current_tier_pool)))
        gcfg.cfg.current_shop.append(populating_card)
        gcfg.pool[populating_card['tier']-1].remove(populating_card)
        populating += 1

#action prompt
def actionp():
    while True:
        print('\n'*3)
        #info for player, + input prompt
        print(f'        Turn {gcfg.turn}')
        print('  <------------------>')
        print('Current shop:') 
        pretty_print(gcfg.cfg.current_shop)
        print('Current board:')
        pretty_print(gcfg.cfg.board)
        print(f'Current gold: {gcfg.cfg.gold}')
        print('Current hand:')
        pretty_print(gcfg.cfg.hand)
        print('  <------------------>')
        gcfg.cfg.action = int(input('Select an action. 0=endturn 1=buy 2=play 3=refresh 4=sell.' + '\n'))
        #buy minion
        if gcfg.cfg.action == 1:
            if gcfg.cfg.gold >= 3:
                gcfg.cfg.gold -= 3
                slot = int(input('Which minion?'))
                gcfg.cfg.current_shop[slot]['id'] = gcfg.curid
                gcfg.curid += 1
                gcfg.cfg.hand.append(gcfg.cfg.current_shop.pop(slot))
                abilities.events.card_added()
            else:
                print('Not enough gold!')
        #play card
        elif gcfg.cfg.action == 2:
            current_slot = int(input('Which card?'))
            current_target = int(input('Play to where?'))
            gcfg.cfg.board.insert(current_target, gcfg.cfg.hand.pop(current_slot))
            card = gcfg.cfg.board[current_target]
            if 'battlecry' in card:
                card['battlecry'](current_target, current_slot)
            if 'spellcast' in card:
                card['spell_cast'](current_target, current_slot)  
            for each_card in gcfg.cfg.board:
                if 'play' in each_card:
                    each_card['play'](gcfg.cfg.board.index(each_card),each_card['type'])
        #refresh
        elif gcfg.cfg.action == 3:
            if gcfg.cfg.gold >= 1:
                gcfg.cfg.gold -= gcfg.cfg.refresh_cost_1
                gcfg.cfg.refresh_cost_1 = gcfg.cfg.refresh_cost_2
                gcfg.cfg.refresh_cost_2 = 1
                refresh_shop()
            else:
                print('Not enough gold!')
        #sell minion
        elif gcfg.cfg.action == 4:
            current_slot = int(input('Which minion?'))
            if 'sold' in gcfg.cfg.board[current_slot]:
                gcfg.cfg.board[current_slot]['sold'](current_slot)
            else:
                abilities.sold.default(current_slot)
        #end turn
        elif gcfg.cfg.action == 0:
            abilities.events.turn_end()
            break
        #other
        else:
            print('Invalid input!')

# makes things look nice
def pretty_print(input):
    for element in input:
        pretty_ver = ''
        if 'attack' in element:
            pretty_ver += f' --- {element["attack"]}/{element["health"]}'
        pretty_ver += f' {element["name"]}'
        print(pretty_ver)



#turn sec
def turn_input():
    cfg = gcfg.cfg
    for minion in gcfg.cfg.board:
        if 'sot' in minion:
            minion['sot']()
    refresh_shop()
    cfg.gold = gcfg.start_gold + gcfg.cfg.bonus_start_turn_gold
    gcfg.cfg.bonus_start_turn_gold = 0
    for minion in gcfg.cfg.board:
        if 'temp_health' in minion:
            minion['health'] -= minion['temp_health']
            del minion['temp_health']
    actionp()