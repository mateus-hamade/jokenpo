import pygame
from pygame.locals import *

from utils import button
from utils import cards
from utils import input_text
from utils import slider
from utils import rotation
from utils import image

def config_first_screen():
    # cria a tela do jogo
    screen = pygame.display.set_mode((960, 582))

    # define um novo cursor
    pygame.mouse.set_visible(False)
    cursor = pygame.image.load('assets/cursor/cursor.png')

    # define o título e o ícone
    pygame.display.set_caption("Jokenpô")

    # carrega as imagens de background
    background = pygame.image.load('assets/images/background.png')
    background = pygame.transform.scale(background, (960, 582))

    # carrega as imagens dos botões
    start_button = button.Button('Iniciar', None, 194, 60, (256, 496), 5)
    exit_button = button.Button('Sair', None, 194, 60, (480, 496), 5)
    config_button = button.Button(' ', 'assets/images/configuracao.png', 194, 60, (810, 10), 5)

    # carrega a música
    music = 'assets/sounds/music/theme_music.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    return screen, cursor, background, start_button, exit_button, config_button	

def config_second_screen():
    # carrega as imagens de background
    background = pygame.image.load('assets/images/connect_screen.png')
    background = pygame.transform.scale(background, (960, 582))

    loading = rotation.ImageAnimation('assets/images/hourglass.png')

    loading_sprite = pygame.sprite.Group()
    loading_sprite.add(loading)

    font = pygame.font.Font('assets/fonts/Quicksand-Bold.ttf', 30)
    waiting = font.render('Aguardando jogador...', True, (255, 255, 255))

    # carrega as botões
    back_button = button.Button('Voltar', None,  194, 60, (480, 496), 5)
    connect_button = button.Button('Conectar', None, 194, 60, (256, 496), 5)

    # carrega os inputs
    input_host = input_text.InputText(364, 300, 164, 50)
    input_name = input_text.InputText(364, 100, 164, 50)

    # carrega textos
    font = pygame.font.Font('assets/fonts/Quicksand-Bold.ttf', 30)
    text_host = font.render('Nome', True, (255, 255, 255))
    text_name = font.render('Servidor', True, (255, 255, 255) )

    return background, loading, loading_sprite, waiting, back_button, connect_button, input_host, input_name, text_host, text_name


def config_third_screen():
    # carrega as imagens de background
    background = pygame.image.load('assets/images/battle_background.png')
    background = pygame.transform.scale(background, (960, 582))

    # carrega as cartas
    rock_card = cards.Card(256, 100, 'assets/images/rock.png')
    paper_card = cards.Card(480, 100, 'assets/images/paper.png')
    scissor_card = cards.Card(704, 100, 'assets/images/scissor.png')

    # carrega as cartas 
    rock_image_card = image.Image('assets/images/rock.png', 369, 195, 90, 119)
    paper_image_card = image.Image('assets/images/paper.png', 369, 195, 90, 119)
    scissor_image_card = image.Image('assets/images/scissor.png', 369, 195, 90, 119)

    enemy_image_card = image.Image('assets/images/enemy_card.jpg', 485, 195, 90, 119)

    # text blink
    font = pygame.font.SysFont(None, 40)
    text_wait = font.render('Aguardando jogada', True, (255, 0, 0))    

    cards_group = pygame.sprite.Group()
    cards_group.add(rock_card)
    cards_group.add(paper_card)
    cards_group.add(scissor_card)

    # carrega a musica
    music = 'assets/sounds/music/battle_music.mp3'
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

    return background, rock_card, paper_card, scissor_card, cards_group, rock_image_card, paper_image_card, scissor_image_card, text_wait, enemy_image_card
    
def config_fourth_screen():
    # carrega as imagens de background
    background = pygame.image.load('assets/images/finish_screen.png')

    # carrega as botões
    back_button = button.Button('Inicio', None,  194, 60, (368, 496), 5)

    return background, back_button, 

def config_settings_screen():
    # carrega as imagens de background
    background = pygame.image.load('assets/images/config_screen.png')
    
    # carrega as botões
    back_button = button.Button('Voltar', None,  194, 60, (383, 496), 5)
    mute_button = button.Button(' ', 'assets/images/mute.png', 194, 60, (810, 10), 5)

    # carrega os sliders
    slider_music = slider.Slider(380, 145.5, 200, 10)

    # carrega textos
    font = pygame.font.Font('assets/fonts/Quicksand-Bold.ttf', 30)
    text_music = font.render('Música', True, (255, 255, 255))

    return background, back_button, mute_button, slider_music, text_music