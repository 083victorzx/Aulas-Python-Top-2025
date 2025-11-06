import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 1440, 900
tela = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()
pygame.display.set_caption("Jogo de Desviar")

# Jogador
jogador = pygame.Rect(100, 700, 10, 10)
cor_jogador = (0, 128, 0)

# Configurações iniciais do jogo
velocidade_jogador = 5
velocidade_obstaculos = 5
freq_obstaculos = 2 # Fase 1: menor frequência = mais fácil
cor_fundo = (50, 50, 50)

# Obstáculos
obstaculos = []

# Controle de tempo
inicio = pygame.time.get_ticks()
ultima_fase = 0  # registra a última fase aplicada
duracao_fase = 0.5  # duração de cada fase em segundos

# Lista de cores para as fases
cores_fases = [
    (50, 50, 50),
    (100, 200, 80),
    (80, 80, 200),
    (200, 50, 50),
    (200, 200, 50)
]

def criar_obstaculo():
    max_tentativas = 10
    for _ in range(max_tentativas):
        x = random.randint(0, largura - 40)
        # Verifica se há outro obstáculo muito próximo horizontalmente
        if all(abs(x - ob.x) > 40 for ob in obstaculos):
            return pygame.Rect(x, -40, 40, 40)
    # Se não conseguir um lugar livre, coloca em posição aleatória mesmo
    return pygame.Rect(random.randint(0, largura - 40), -40, 40, 40)

rodando = True
while rodando:
    # Tempo decorrido em segundos
    tempo_decorrido = (pygame.time.get_ticks() - inicio) / 1000

    # Determinar fase atual
    fase_atual = int(tempo_decorrido // duracao_fase)

    # Atualizar velocidade, frequência e cor a cada fase
    if fase_atual > ultima_fase:
        ultima_fase = fase_atual
        velocidade_obstaculos += 0  # aumenta a velocidade dos obstáculos
        velocidade_jogador += 0      # jogador também fica um pouco mais rápido
        # freq_obstaculos = max(5, freq_obstaculos - 5)  # aumenta frequência (menor valor = mais obstáculos)
        cor_fundo = cores_fases[fase_atual % len(cores_fases)]  # muda a cor do fundo

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador.left > 0:
        jogador.x -= velocidade_jogador
    if teclas[pygame.K_RIGHT] and jogador.right < largura:
        jogador.x += velocidade_jogador

    # Criar obstáculos aleatórios
    if random.randint(1, freq_obstaculos) == 1:
        obstaculos.append(criar_obstaculo())

    # Atualizar obstáculos
    for obstaculo in obstaculos:
        obstaculo.y += velocidade_obstaculos
        if jogador.colliderect(obstaculo):
            rodando = False
        pygame.draw.rect(tela, (0,0, 0), obstaculo)

    # Remover obstáculos que saíram da tela
    obstaculos = [ob for ob in obstaculos if ob.y < altura]

    # Desenhar jogador e atualizar tela
    tela.fill(cor_fundo)
    pygame.draw.rect(tela, cor_jogador, jogador)
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, (255,255,255),obstaculo)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()