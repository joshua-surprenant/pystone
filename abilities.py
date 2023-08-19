import gcfg
import random
import cfg1
import cfg2
from operator import itemgetter

#all abilities
class keywords:
    def taunt_check():
            return True
    def reborn(current_board, current_slot, minion):
        minion['health'] = 1
        minion['name'] += ' (Reborn)'
        minion['has_reborn'] = False
        gcfg.combat_board[current_board].insert(current_slot, minion)
class sold:
    def default(current_slot):
        gcfg.cfg.gold += 1
        for minion in minion_list:
            if gcfg.cfg.board[current_slot]['name'] == minion['name']:
                gcfg.pool[minion['tier']-1].append(minion)
                del gcfg.cfg.board[int(current_slot)]
                break
    def sellemental(current_slot):
        sold.default(current_slot)
        gcfg.cfg.hand.append({'name':'WaterDroplet','attack':2,'health':2,'type':'Elemental','tier':1})
        events.card_added()
    def sunbacon_relaxer(current_slot):
        sold.default(current_slot)
        i=0
        while i<2:
            gcfg.cfg.hand.append({'name':'BloodGem','spell_cast':spell_cast.blood_gem})
            events.card_added()
            i+=1
class eot:
    def micro_mummy(current_slot):
        board_without_self = [x for i,x in enumerate(gcfg.cfg.board) if i!=current_slot]
        if board_without_self != []:
            random.choice(board_without_self)[2] += 1
    def upbeat_frontdrake(current_slot):
        if gcfg.cfg.board[current_slot]['counter'] < 1:
            dragon_pool = []
            for card in gcfg.pool:
                if 'Dragon' in card['type']:
                    dragon_pool += card
            gcfg.cfg.hand.append(random.randchoice(dragon_pool))
        else:
            gcfg.cfg.board[current_slot]['counter'] -= 1
class deathrattle:
    def imprisoner(current_board, current_slot):
        gcfg.combat_board[current_board].insert(current_slot, {'name':'Imp','attack':1,'health':1,'type':['Demon'],'tier':1})
    def manasaber(current_board, current_slot):
        gcfg.combat_board[current_board].insert(current_slot, {'name':'Cubling','attack':0,'health':1,'type':['Beast'],'tier':1}) 
        gcfg.combat_board[current_board].insert(current_slot, {'name':'Cubling','attack':0,'health':1,'type':['Beast'],'tier':1}) 
    def scallywag(current_board, current_slot):
        gcfg.combat_board[current_board].insert (current_slot, {'name':'Pirate','attack':1,'health':1,'type':['Pirate'],'tier':1})
        print(f"Player 1's board is:{gcfg.combat_board[0]}")
        print(f"Player 2's board is:{gcfg.combat_board[1]}")
        events.attack(int(not(current_board)),int(current_board),current_slot)
        events.kill_dead_minions(current_slot)
class battlecry:
    def picky_eater(current_target, current_slot):
        eating = gcfg.cfg.current_shop.pop(random.randrange(len(gcfg.cfg.current_shop)))
        gcfg.cfg.board[current_target]['attack'] += eating['attack']
        gcfg.cfg.board[current_target]['health'] += eating['health']
    def shell_collector(current_target, current_slot):
        gcfg.cfg.hand.append({'name':'Gold Coin','spell_cast':spell_cast.gold_coin})
        events.card_added()
    def southsea_busker(current_target, current_slot):
        gcfg.cfg.bonus_start_turn_gold += 1
    def razorfen_geomancer(current_target, current_slot):
        gcfg.cfg.hand.append({'name':'BloodGem','spell_cast':spell_cast.blood_gem})
        events.card_added()
    def rockpool_hunter(current_target, current_slot):
        target = input('Choose a murloc to buff:')
        if 'Murloc' in gcfg.cfg.board[target]['type']:
            gcfg.cfg.board[target]['attack'] += 1
            gcfg.cfg.board[target]['health'] += 1
        else:
            print('Invalid input! Not a murloc.')
    def refreshing_anomaly(current_target, current_slot):
        gcfg.cfg.refresh_cost_1 = 0
class draw:
    def thorncaptain(slot):
        gcfg.cfg.board[slot]['health'] += 1
        if 'temp_health' in gcfg.cfg.board[slot]:
            gcfg.cfg.board[slot]['temp_health'] += 1
        else:
            gcfg.cfg.board[slot]['temp_health'] = 1
class attacked:
    def dozy_whelp(current_board, current_slot, id):
        gcfg.combat_board[current_board][current_slot]['attack']+=1
        if current_board == 0:
            player = cfg1
        if current_board == 1:
            player = cfg2
        for card in player.board:
            if id == card['id']:
                card['attack'] += 1
class spellcraft:
    def minimyrmidon():
        gcfg.cfg.hand.append(['MiniMyrmidonSpellcraft'])
        events.card_added()
class spell_cast:
    def minimyrmidon(current_target, current_slot):
        del gcfg.cfg.board[current_target]
        gcfg.cfg.board[current_target][1] += 2
    def blood_gem(current_target, current_slot):
        del gcfg.cfg.board[current_target]
        gcfg.cfg.board[current_target][1] += gcfg.cfg.blood_gem_stats[0]
        gcfg.cfg.board[current_target][2] += gcfg.cfg.blood_gem_stats[1]
    def gold_coin(current_target, current_slot):
        gcfg.cfg.gold += 1
class die:
    def scavenging_hyena(current_board, current_slot, id, dead_min_type):
        if 'Beast' in dead_min_type:
            gcfg.combat_board[current_board][current_slot]['attack']+=2
            gcfg.combat_board[current_board][current_slot]['health']+=1
class play:
    def swampstriker(current_slot, type_played):
        if 'Murloc' in type_played:
            gcfg.cfg.board[current_slot]['attack'] += 1
    def wrath_weaver(current_slot, type_played):
        if 'Demon' in type_played:
            gcfg.cfg.health -= 1
            gcfg.cfg.board[current_slot]['attack'] += 2
            gcfg.cfg.board[current_slot]['health'] += 1
class sot:
    def backstage_security():
        gcfg.cfg.health -= 1
    
#events (end of turn, card drawn, etc)
class events:
    def card_added():
        for card in gcfg.cfg.board:
            if 'draw' in card:
                card['draw'](gcfg.cfg.board.index(card))
    def turn_end():
        for card in gcfg.cfg.board:
            if 'eot' in card:
                card['eot'](gcfg.cfg.board.index(card))
    def attack(defending_player, attacking_player, attacking_slot):
        #choose target, check taunts
        taunt_minions = []
        for minion in gcfg.combat_board[defending_player]:
            if 'taunt' in minion:
                taunt_minions.append(minion)
        if taunt_minions == [None] or taunt_minions == []:
            attacking_target = random.randint(0,len(gcfg.combat_board[defending_player])-1)
            attacking_target_minion = gcfg.combat_board[defending_player][attacking_target]
        else:
            attacking_target = gcfg.combat_board[defending_player].index(random.choice(taunt_minions))
            attacking_target_minion = gcfg.combat_board[defending_player][attacking_target]
        #deal damage
        gcfg.combat_board[defending_player][attacking_target]['health']-=gcfg.combat_board[attacking_player][attacking_slot]['attack']
        gcfg.combat_board[attacking_player][attacking_slot]['health']-=gcfg.combat_board[defending_player][attacking_target]['attack']
        #attacked trigger
        if 'attacked' in attacking_target_minion:
            attacking_target_minion['attacked'](gcfg.combat_board.index(gcfg.combat_board[defending_player]),gcfg.combat_board[defending_player].index(attacking_target_minion),attacking_target_minion['id'])
    def kill_dead_minions(attacking_slot):
        for board in gcfg.combat_board:
            for minion in board:
                if minion['health'] < 1:
                    current_board = gcfg.combat_board.index(board)
                    current_slot = board.index(minion)
                    if current_slot < attacking_slot:
                        attacking_slot -= 1
                    del board[current_slot]
                    gcfg.combat_deaths += 1
                    for minion_die_trigger in board:
                        if 'die' in minion_die_trigger:
                            minion_die_trigger['die'](current_board,current_slot,minion_die_trigger['id'],minion['type'])
                    if 'deathrattle' in minion:
                        minion['deathrattle'](current_board,current_slot)
                    if 'has_reborn' in minion:
                        if minion['has_reborn'] == True:
                            keywords.reborn(current_board,current_slot,minion)

#all default minion values
minion_list = [
#{'name':,'attack':,'health','type':[],'tier':1,'taunt':,'reborn':,'deathrattle':,'battlecry':,'attacked':,'attack':,'sold':,'draw':,'sell':,'play':,}
#{'name':'','attack':,'health':,'type':[''],'tier':2,},
# t1
{'name':'Dozy Whelp','attack':0,'health':3,'type':['Dragon'],'tier':1,'attacked':attacked.dozy_whelp,'taunt':True},
{'name':'Imprisoner','attack':2,'health':2,'type':['Demon'],'tier':1,'taunt':True,'deathrattle':deathrattle.imprisoner},
{'name':'Manasaber','attack':4,'health':1,'type':['Beast'],'tier':1,'deathrattle':deathrattle.manasaber},
{'name':'Micro Mummy','attack':1,'health':2,'type':['Mech','Undead'],'tier':1,'has_reborn':True,'eot':eot.micro_mummy},
{'name':'Mini-Myrmidon','attack':1,'health':2,'type':['Naga'],'tier':1,'spellcraft':spellcraft.minimyrmidon},
{'name':'Mistake','attack':1,'health':3,'type':['Demon','Beast','Naga','Dragon','Quilboar','Undead','Mech','Murloc','Elemental','Pirate'],'tier':1,},
{'name':'Picky Eater','attack':1,'health':1,'type':['Demon'],'tier':1,'battlecry':battlecry.picky_eater},
{'name':'Razorfen Geomancer','attack':3,'health':1,'type':['Quilboar'],'tier':1,'battlecry':battlecry.razorfen_geomancer},
{'name':'Refreshing Anomaly','attack':1,'health':4,'type':['Elemental'],'tier':1,'battlecry':battlecry.refreshing_anomaly},
{'name':'Risen Rider','attack':2,'health':1,'type':['Undead'],'tier':1,'taunt':True,'has_reborn':True},
{'name':'Rockpool Hunter','attack':2,'health':3,'type':['Murloc'],'tier':1,'battlecry':battlecry.rockpool_hunter},
{'name':'Rot Hide Gnoll','attack':1+gcfg.combat_deaths,'health':4,'type':['Undead'],'tier':1},
{'name':'Scallywag','attack':3,'health':1,'type':['Pirate'],'tier':1,'deathrattle':deathrattle.scallywag},
{'name':'Scavenging Hyena','attack':2,'health':2,'type':['Beast'],'tier':1,'die':die.scavenging_hyena},
{'name':'Sellemental','attack':2,'health':2,'type':['Elemental'],'tier':1,'sold':sold.sellemental},
{'name':'Shell Collector','attack':2,'health':1,'type':['Naga'],'tier':1,'battlecry':battlecry.shell_collector},
{'name':'Southsea Busker','attack':3,'health':1,'type':['Pirate'],'tier':1,'battlecry':battlecry.southsea_busker},
{'name':'Sun-Bacon Relaxer','attack':1,'health':2,'type':['Quilboar'],'tier':1,'sold':sold.sunbacon_relaxer},
{'name':'Swampstriker','attack':1,'health':4,'type':['Murloc'],'tier':1,'play':play.swampstriker},
{'name':'Thorncaptain','attack':4,'health':2,'type':['Quilboar','Pirate'],'tier':1,'draw':draw.thorncaptain},
{'name':'Upbeat Frontdrake','attack':1,'health':1,'type':['Dragon'],'tier':1,'eot':eot.upbeat_frontdrake,'counter':3},
{'name':'Wrath Weaver','attack':1,'health':4,'type':[],'tier':1,'play':play.wrath_weaver},
# t2
{'name':'Backstage Security','attack':4,'health':6,'type':['Demon'],'tier':2,'sot':sot.backstage_security},
]

