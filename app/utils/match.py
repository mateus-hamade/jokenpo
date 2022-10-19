class Match:
    def __init__(self):
        self.client_socket = None                       # Client socket
        self.host = None                                # Host IP
        self.data_input = ''                            # Dados recebidos do cliente
        
        self.rounds = 1                                 # Rodadas jogadas
        self.waiting_player = False                     # Se está esperando um jogador
        self.connection_allowed = False                 # Se dois jogadores estão conectados é permitido iniciar a partida

        self.jokenpo = ["rock", "paper", "scissor"]     # Opções de jogada

class Player:
    def __init__(self):
        self.username = ''      # nome do jogador
        self.life = 3           # vida do jogador
        self.move = ''          # movimento do jogador (carta)
        self.movement = False   # movimento do jogador (verificação)