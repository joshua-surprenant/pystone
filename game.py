#---to do---
# make scallywag work at all
# bug hunt (added like 1000 things and didnt test any of them sure i wont regret this)

import gcfg
import cfg1
import cfg2
import turn
import pygame
from sys import exit

# set up pygame / screen
pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('Pystone')
clock = pygame.time.Clock()
test_font = pygame.font.Font('assets/Belwe Medium.otf', 50)


background_surf = pygame.Surface((1920,1080))
#picky_eater_surf = 
# 200p deadspace, 8 215p spaces between cards
picky_eater_rect = pygame.transform.scale(pygame.image.load('assets/cards/picky_eater.png'), ((202,279))).get_rect(midbottom = (415, 400))
title_surf = test_font.render(f'Turn {gcfg.turn}', True, 'White')
title_rect = title_surf.get_rect(midbottom = (960, 100))

current_player = 0
gcfg.cfg.turn_over = False
turn.create_pool()
turn.turn_input()
glow_opacity = {'board':[0,0,0,0,0,0,0],'hand':[0,0,0,0,0,0,0,0,0,0],'shop':[0,0,0,0,0,0,0]}
mouse_last_pos = False

def display_cards(source, display_y):
            i=0
            display_x = 1920/(len(source)+1)
            if source == gcfg.cfg.current_shop:
                source_str = 'shop'
            if source == gcfg.cfg.board:
                source_str = 'board'
            if source == gcfg.cfg.hand:
                source_str = 'hand'
            while i < len(source):
                global glow_opacity
                global mouse_last_pos
                minion = source[i]
                card_surf = pygame.transform.scale(pygame.image.load(minion['sprite']), ((202,279)))
                card_rect = card_surf.get_rect(midbottom = (display_x, display_y))
                # glow_surf = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('assets/glow.png'), 90), ((404,558)))
                # glow_rect = glow_surf.get_rect(midbottom = (display_x, display_y+150))
                if card_rect.collidepoint(mouse_pos):
                #     if glow_opacity[source_str][i] < 255:
                #         glow_opacity[source_str][i] += 30
                    if pygame.mouse.get_pressed()[0] == True:
                        if mouse_last_pos == False:
                            if source_str == 'shop':
                                turn.player_actions.buy_minion(i)
                            if source_str == 'hand':
                                turn.player_actions.play_card(i, 0)
                        mouse_last_pos = True
                    else:
                        mouse_last_pos = False
                # else:
                #     if glow_opacity[source_str][i] > 0:
                #         glow_opacity[source_str][i] -= 30
                # glow_surf.set_alpha(glow_opacity[source_str][i])
                # screen.blit(glow_surf, glow_rect)
                screen.blit(card_surf, card_rect)
                display_x += (1920 - (len(source)))/(len(source)+1)
                i += 1


while True:
    shop_x = 0
    if gcfg.cfg.turn_over == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        i=0


        mouse_pos = pygame.mouse.get_pos()

        screen.blit(background_surf,(0,0))

        
        

        

        # for each item in the shop, display that item
        display_cards(gcfg.cfg.current_shop, 400)
        display_cards(gcfg.cfg.hand, 1050)
        display_cards(gcfg.cfg.board, 725)
        screen.blit(title_surf, title_rect)

        pygame.display.update()
        clock.tick(60)
    else:
        current_player += 1
        gcfg.cfg = __import__(gcfg.pl[current_player])
        gcfg.cfg.turn_over = False


game_going = True


# for each turn
def loop():
    win_check()
    #for each player, set current player and play
    for player in gcfg.player_list:
        gcfg.cfg = __import__(player)
        turn.turn_input()
    #combat
    import combat
    if gcfg.start_gold < 10:
        gcfg.start_gold += 1

def win_check():
    if cfg1.health < 1:
        game_winner = 'Player 1'
        game_going = False
    if cfg2.health < 1:
        game_winner = 'Player 2'
        game_going = False
 

#print(f'Game over! {game_winner} wins!')