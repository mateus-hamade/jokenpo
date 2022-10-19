# bibliotecas para socker e threading
import socket
import threading

# bibliotecas da interface
import pyautogui
import pygame
from pygame.locals import *

# elementos da interface
from utils import settings
from utils import image
from utils.match import Match, Player

cursor = pygame.image.load('assets/cursor/cursor.png')

PERMISSION = True
SHOW_CARD = False

def receive(partida = Match(), jogador1 = Player(), jogador2 = Player()):
    while True:
        try:
            data_input = partida.client_socket.recv(1024) # recebe os dados

            verify_data(data_input, partida, jogador1, jogador2)
        except:
            if data_input == b"exit":
                partida.client_socket.shutdown(socket.SHUT_RDWR)
                partida.client_socket.close()
            return

def send(partida = Match()):
    while True:
        try:
            while True:
                data_output = input('\n') 
                if data_output == "exit" or partida.data_input == b"exit":
                    raise
                elif data_output in partida.jokenpo:
                    break
            partida.client_socket.send(data_output.encode())
        except:
            print("Client disconnected")
            if partida.data_input == b"exit":
                return
            partida.client_socket.shutdown(socket.SHUT_RDWR)
            partida.client_socket.close()
            return

def connect_server(partida = Match(), jogador1 = Player()):
    port = 62000
    addr = (partida.host, port)

    partida.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: # tenta conectar ao servidor
        partida.client_socket.connect(addr)
        if partida.client_socket.recv(1024) == b'0':
            pyautogui.alert(text='Servidor cheio', title='Erro', button='OK')
            raise 
    except Exception as e:
        print(e)
        pyautogui.alert(text='Erro ao conectar ao servidor!', title='Error', button='OK')

    while True: # atenção
        partida.client_socket.send(jogador1.username.encode())
        if partida.client_socket.recv(1024) == b'0':
            pyautogui.alert(text='Nome já está em uso', title='Erro', button='OK')
        else:
            break

    if (partida.client_socket.recv(1024) == b'0'): # espera o outro jogador entrar na sala
        while True:
            partida.waiting_player = True
            if partida.client_socket.recv(1024) == b'2':
                partida.waiting_player = False
                break

    partida.connection_allowed = True

def verify_data(data_input, partida = Match(), jogador1 = Player(), jogador2 = Player()):
    global PERMISSION
    global SHOW_CARD

    # incrementa o número de rodadas
    if data_input == b'round': 
        partida.rounds = str(int(partida.rounds) + 1)

    # decrementa a vida do jogador 1
    if data_input == jogador1.username.encode():
        jogador1.life = str(int(jogador1.life) - 1)
    
    # decrementa a vida do jogador 2
    if data_input == jogador2.username.encode():
        jogador2.life = str(int(jogador2.life) - 1)

    # recebe o movimento do oponente
    if data_input.decode().count('.move') > 0:
        jogador2.move = data_input.decode().split('.')[0]

    # recebe se o oponente jogou
    if data_input.decode().count('.moviment') > 0:
        jogador2.movement = True    

    # recebe o nome do oponente
    if data_input.decode().count('?') > 0:
        jogador2.username = data_input.decode().split('?')[0]

    if data_input.decode().count('.false') > 0:
        jogador2.movement = False
        PERMISSION = False
        SHOW_CARD = True

    if data_input.decode().count('.release') > 0:
        jogador1.move = 'None'
        jogador2.move = 'None'

        SHOW_CARD = False
        PERMISSION = True

def start_screen():
    # inicia a tela
    pygame.init()

    # recebe as configurações do arquivo settings.py
    screen, cursor, background, start_button, exit_button, config_button = settings.config_first_screen()

    # loop principal da tela inicial
    running = True
    return_first_screen = True
    while running or return_first_screen:
        # desenha o background
        screen.blit(background, (0, 0))

        # desenha os botões
        exit_button.draw(screen)
        start_button.draw(screen)
        config_button.draw(screen)
        
        # desenha o cursor
        screen.blit(cursor, pygame.mouse.get_pos())

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    running = connect_screen(screen)

                    # verificar depois 
                    if running and not return_first_screen:
                        pygame.mixer.Sound('assets/sounds/sfx/theme_music.mp3').play()

                elif config_button.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    running, return_first_screen = settings_screen(screen)

                elif exit_button.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()
                    
                    running = False
                    return_first_screen = False

            if event.type == QUIT: # exit
                running = False
                return_first_screen = False

        pygame.display.update() # update screen
    
    pygame.quit()

def connect_screen(screen):
    # cria as partidas e os jogadores
    partida = Match()
    jogador1 = Player()
    jogador2 = Player()

    # recebe as configurações do arquivo settings.py
    background, loading, loading_sprite, waiting, back_button, connect_button, input_host, input_name, text_host, text_name = settings.config_second_screen()

    # loop principal da tela de conexão
    running = True
    while running:
        if partida.waiting_player: # se o jogador estiver esperando o outro jogador atualiza para tela de espera
            clock = pygame.time.Clock() # clock para animação
            clock.tick(20)

            # animação de loading
            loading.turnRight() 
            loading_sprite.clear(screen, background) 
            
            # desenha o background
            screen.fill((0, 0, 0))
            
            # atuliza a tela
            loading_sprite.update()
            loading_sprite.draw(screen)
        
            # desenha o texto
            screen.blit(waiting, (330, 440))
        else:
            # desenha o background
            screen.blit(background, (0, 0))

            # desenha os botões
            back_button.draw(screen)
            connect_button.draw(screen)

            # desenha os textos
            screen.blit(text_host, (364, 50))
            screen.blit(text_name, (364, 250))
       
        # eventos
        for event in pygame.event.get():
            input_host.handle_event(event)
            input_name.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if connect_button.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    jogador1.username = input_name.return_text()
                    partida.host = input_host.return_text()
                
                    if not jogador1.username:
                        pyautogui.alert(text='Digite um nome válido', title='Erro', button='OK')
                    elif partida.host != '26.97.160.140': 
                        pyautogui.alert(text='Digite um servidor válido', title='Erro', button='OK')
                    else:
                        threading.Thread(target=connect_server, args=(partida, jogador1)).start()

                elif back_button.check_click():    
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    return False, True
                    
            if event.type == QUIT:
                running = False
            
            if partida.connection_allowed:
                threading.Thread(target=receive, args=[partida, jogador1, jogador2]).start()

                running = play_screen(screen, partida, jogador1, jogador2)
                
                if running == False:
                    return False

        if not partida.waiting_player:
            # draw inputs
            input_host.draw(screen)
            input_name.draw(screen)

            input_host.update()
            input_name.update()

            font = pygame.font.SysFont('assets/fonts/Quicksand-Bold.ttf', 35)
            name_allowed = font.render('OK', True, (0, 255, 0))
            host_allowed = font.render('OK', True, (0, 255, 0))

            if input_name.return_text():
                screen.blit(name_allowed, (584, 114))
            if input_host.return_text() != '26.97.160.140':
                screen.blit(host_allowed, (585, 322))

        screen.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update() # update screen

    return False, False

def play_screen(screen, partida = Match(), jogador1 = Player(), jogador2 = Player()):
    global PERMISSION
    global SHOW_CARD

    # recebe as configurações do arquivo settings.py
    background, rock_card, paper_card, scissor_card, cards_group, rock_image_card, paper_image_card, scissor_image_card, text_wait, enemy_image_card = settings.config_third_screen()

    # configurações do texto 
    font_fade = pygame.USEREVENT + 1
    pygame.time.set_timer(font_fade, 400)
    show_text = True

    # loop principal da tela de jogo
    running = True
    while running:
        # desenha o background      
        screen.blit(background, (0, 0))

        # events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and PERMISSION:
                if rock_card.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    partida.client_socket.send(b'rock')
                    jogador1.move = 'rock'
                elif paper_card.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    partida.client_socket.send(b'paper')
                    jogador1.move = 'paper'
                elif scissor_card.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    partida.client_socket.send(b'scissor')
                    jogador1.move = 'scissor'
            if event.type == font_fade:
                show_text = not show_text
            
            if event.type == QUIT:
                partida.client_socket.send('quit'.encode())
                running = False

        # update
        cards_group.update()

        # draw cards
        cards_group.draw(screen)

        # atualiza a tela com as informações
        screen.blit(pygame.font.SysFont('assets/fonts/Quicksand-Bold.ttf', 60).render(str(partida.rounds), True, (255, 16, 27)), (36, 273))
        screen.blit(pygame.font.SysFont('assets/fonts/Quicksand-Bold.ttf', 50).render(str(jogador1.life), True, (255, 255, 255)), (36, 336))
        screen.blit(pygame.font.SysFont('assets/fonts/Quicksand-Bold.ttf', 50).render(str(jogador2.life), True, (255, 255, 255)), (36, 213))

        # desenha a carta do jogador
        if jogador1.move == 'rock':
            rock_image_card.draw(screen)
        elif jogador1.move == 'paper':
            paper_image_card.draw(screen)
        elif jogador1.move == 'scissor':
            scissor_image_card.draw(screen)

        if jogador2.movement:
            if show_text:
                screen.blit(text_wait, (342, 86))

            enemy_image_card = image.Image('assets/images/enemy_card.jpg', 485, 195, 90, 119)
            enemy_image_card.draw(screen)


        if SHOW_CARD:
            if jogador2.move == 'rock':
                enemy_image_card = image.Image('assets/images/rock.png', 485, 195, 90, 119)
                enemy_image_card.draw(screen)
            elif jogador2.move == 'paper':
                enemy_image_card = image.Image('assets/images/paper.png', 485, 195, 90, 119)
                enemy_image_card.draw(screen)
            elif jogador2.move == 'scissor':
                enemy_image_card = image.Image('assets/images/scissor.png', 485, 195, 90, 119)
                enemy_image_card.draw(screen)

        if int(jogador1.life) == 0 or int(jogador2.life) == 0 or int(partida.rounds) > 5:
            running = finish_screen(screen, partida, jogador1, jogador2)

        #cursor
        screen.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update() # update screen

    return False

def finish_screen(screen, partida = Match(), jogador1 = Player(), jogador2 = Player()):
    # recebe as configurações do arquivo settings.py
    background, back_button = settings.config_fourth_screen()

    font = pygame.font.Font('assets/fonts/Quicksand-Bold.ttf', 60)
    if int(jogador1.life) > int(jogador2.life):
        text_situation = font.render(f'{jogador1.username} Ganhou !!!', True, (64, 60, 96))
    elif int(jogador1.life) < int(jogador2.life):
        text_situation = font.render(f'{jogador1.username} Perdeu !!!', True, (64, 60, 96))
    else:
        text_situation = font.render('Empate !!!', True, (64, 60, 96))

    running = True
    while running:
        # desenha o background
        screen.blit(background, (0, 0))

        # desenha os botões
        back_button.draw(screen)

        # desenha o texto
        screen.blit(text_situation, (334, 92))

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    partida.client_socket.send('quit'.encode())
                    running = False
                    
            if event.type == pygame.QUIT:
                partida.client_socket.send('quit'.encode())
                return False, False

        #cursor
        screen.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update()

    return False

def settings_screen(screen):
    # recebe as configurações do arquivo settings.py
    background, back_button, mute_button, slider_music, text_music = settings.config_settings_screen()

    mute = False

    # loop principal da tela de configurações
    running = True
    while running:
        # desenha o background
        screen.blit(background, (0, 0))

        # desenha os botões
        mute_button.draw(screen)
        back_button.draw(screen)

        # desenha os textos
        screen.blit(text_music, (430, 70))

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if slider_music.on_slider_hold(event.pos[0], event.pos[1]):
                    slider_music.handle_event(screen, event.pos[0])
                elif back_button.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    return False, True
                elif mute_button.check_click():
                    pygame.mixer.Sound('assets/sounds/sfx/click.mp3').play()

                    mute = not mute
                    pygame.mixer.music.set_volume(0)
            if event.type == pygame.MOUSEMOTION:
                if slider_music.on_slider(event.pos[0], event.pos[1]):
                    slider_music.handle_event(screen, event.pos[0])

        if not mute:
            pygame.mixer.music.set_volume(slider_music.get_volume() / 100.0)

        # draw sliders
        slider_music.draw(screen)

        #cursor
        screen.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update() 

    return False, False

if __name__ == "__main__":
    start_screen()