import pygame
import random

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA = 600
ALTURA = 400
TAMANHO_QUADRADO = 20

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🐍 Snake Game")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Fonte
fonte = pygame.font.SysFont("Arial", 25, True)

# Função para desenhar a cobra
def desenhar_cobra(tamanho, lista_corpo):
    for x, y in lista_corpo:
        pygame.draw.rect(tela, VERDE, (x, y, tamanho, tamanho))

# Função para mostrar o placar
def mostrar_pontuacao(pontos):
    texto = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto, (10, 10))

# Função principal do jogo
def jogo():
    fim_de_jogo = False
    sair = False

    # posição inicial da cobra
    x = LARGURA // 2
    y = ALTURA // 2
    x_vel = 0
    y_vel = 0

    corpo_cobra = []
    tamanho_cobra = 1

    # velocidade inicial da cobra (agora dentro da função)
    velocidade = 10

    # Posição inicial da comida
    comida_x = round(random.randrange(0, LARGURA - TAMANHO_QUADRADO) / 20.0) * 20
    comida_y = round(random.randrange(0, ALTURA - TAMANHO_QUADRADO) / 20.0) * 20

    clock = pygame.time.Clock()

    while not sair:
        while fim_de_jogo:
            tela.fill(PRETO)
            msg = fonte.render("Game Over! Pressione R para reiniciar ou Q para sair", True, VERMELHO)
            tela.blit(msg, (LARGURA / 2 - 250, ALTURA / 2 - 30))
            mostrar_pontuacao(tamanho_cobra - 1)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sair = True
                    fim_de_jogo = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        sair = True
                        fim_de_jogo = False
                    if evento.key == pygame.K_r:
                        jogo()

        # Movimentação
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x_vel == 0:
                    x_vel = -TAMANHO_QUADRADO
                    y_vel = 0
                elif evento.key == pygame.K_RIGHT and x_vel == 0:
                    x_vel = TAMANHO_QUADRADO
                    y_vel = 0
                elif evento.key == pygame.K_UP and y_vel == 0:
                    y_vel = -TAMANHO_QUADRADO
                    x_vel = 0
                elif evento.key == pygame.K_DOWN and y_vel == 0:
                    y_vel = TAMANHO_QUADRADO
                    x_vel = 0

        x += x_vel
        y += y_vel

        # Verifica colisão com as bordas
        if x >= LARGURA or x < 0 or y >= ALTURA or y < 0:
            fim_de_jogo = True

        tela.fill(PRETO)

        # Desenha a comida
        pygame.draw.rect(tela, AZUL, (comida_x, comida_y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        # Atualiza corpo da cobra
        cabeca_cobra = [x, y]
        corpo_cobra.append(cabeca_cobra)
        if len(corpo_cobra) > tamanho_cobra:
            del corpo_cobra[0]

        # Verifica colisão com o próprio corpo
        for parte in corpo_cobra[:-1]:
            if parte == cabeca_cobra:
                fim_de_jogo = True

        desenhar_cobra(TAMANHO_QUADRADO, corpo_cobra)
        mostrar_pontuacao(tamanho_cobra - 1)

        pygame.display.update()

        # Quando come a comida
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, LARGURA - TAMANHO_QUADRADO) / 20.0) * 20
            comida_y = round(random.randrange(0, ALTURA - TAMANHO_QUADRADO) / 20.0) * 20
            tamanho_cobra += 1
            velocidade += 0.5  # aumenta um pouco a velocidade a cada comida

        clock.tick(velocidade)

    pygame.quit()

# Inicia o jogo
jogo()
