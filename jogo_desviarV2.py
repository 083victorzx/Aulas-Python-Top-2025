import pygame
import random
import time as t

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 400, 600
tela = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()
pygame.display.set_caption("Jogo de Desviar")

# Carregar imagem de fundo
fundo = pygame.image.load("fundo_espaco.jpeg")
fundo = pygame.transform.scale(fundo, (largura, altura))

# Jogador
jogador = pygame.Rect((largura/2) - 20, altura - 100, 40, 40)
cor_jogador = (0, 128, 0)

# Configurações iniciais do jogo
velocidade_jogador = 10
velocidade_obstaculos = 10
freq_obstaculos = 35

# Obstáculos e balas
obstaculos = []
balas = []

# Controle de tempo
inicio = pygame.time.get_ticks()
tempo = 0
debounce = 0

def criar_obstaculo():
    max_tentativas = 10
    for _ in range(max_tentativas):
        x = random.randint(0, largura - 40)
        if all(abs(x - ob.x) > 40 for ob in obstaculos):
            return pygame.Rect(x, -40, 40, 40)
    return pygame.Rect(random.randint(0, largura - 40), -40, 40, 40)

def tela_game_over():
    fonte = pygame.font.SysFont(None, 40)
    texto1 = fonte.render("GAME OVER", True, (255, 0, 0))
    texto2 = fonte.render("R - Recomeçar", True, (255, 255, 255))
    texto3 = fonte.render("S - Sair", True, (255, 255, 255))

    while True:
        tela.blit(fundo, (0, 0))
        tela.blit(texto1, (100, 200))
        tela.blit(texto2, (80, 300))
        tela.blit(texto3, (120, 350))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True      # Recomeça
                if evento.key == pygame.K_s:
                    pygame.quit()
                    exit()

def loop_jogo():
    global obstaculos, balas, inicio, tempo, debounce

    # Variáveis reiniciadas ao começar o jogo
    obstaculos = []
    balas = []
    jogador.x = largura//2 - 20

    inicio = pygame.time.get_ticks()
    tempo = 0
    debounce = 0

    # Agora definimos aqui dentro!
    velocidade_obstaculos = 10
    velocidade_jogador = 10
    freq_obstaculos = 30

    rodando = True

    while rodando:
        tempo_decorrido = (pygame.time.get_ticks() - inicio) / 1000

        # Aumenta dificuldade a cada 3 segundos
        if (tempo_decorrido - tempo) >= 3:
            tempo = tempo_decorrido
            velocidade_obstaculos += 1
            freq_obstaculos = max(5, freq_obstaculos - 1)

        recarregamento = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Movimento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador.left > 0:
            jogador.x -= velocidade_jogador
        if teclas[pygame.K_RIGHT] and jogador.right < largura:
            jogador.x += velocidade_jogador

        # Tiro
        if teclas[pygame.K_e] and (recarregamento - debounce) > 500:
            debounce = recarregamento
            balas.append(pygame.Rect(jogador.x + 15, jogador.y - 10, 10, 10))

        # Criar obstáculos
        if random.randint(1, freq_obstaculos) == 1:
            obstaculos.append(criar_obstaculo())

        # Atualizar balas e obstáculos
        balas = [b for b in balas if b.y > 0]

        for obstaculo in obstaculos:
            obstaculo.y += velocidade_obstaculos
            if jogador.colliderect(obstaculo):
                rodando = False

        for bala in balas[:]:
            bala.y -= 10
            for obstaculo in obstaculos[:]:
                if bala.colliderect(obstaculo):
                    balas.remove(bala)
                    obstaculos.remove(obstaculo)
                    break

        obstaculos = [ob for ob in obstaculos if ob.y < altura]

        # Desenho
        tela.blit(fundo, (0, 0))
        pygame.draw.rect(tela, cor_jogador, jogador)

        for obstaculo in obstaculos:
            pygame.draw.rect(tela, (255, 0, 0), obstaculo)
        for b in balas:
            pygame.draw.rect(tela, (255, 255, 255), b)

        pygame.display.flip()
        clock.tick(60)

    return False

# LOOP PRINCIPAL DO JOGO
while True:
    perdeu = not loop_jogo()
    if perdeu:
        if not tela_game_over():
            break
