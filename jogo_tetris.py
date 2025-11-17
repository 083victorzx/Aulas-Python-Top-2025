import pygame, random

# Inicialização do pygame
pygame.init()

# Configurações da tela
TAMANHO_BLOCO = 30
COLUNAS, LINHAS = 10, 20
LARGURA_JOGO = COLUNAS * TAMANHO_BLOCO
LARGURA_PAINEL = 200
ALTURA = LINHAS * TAMANHO_BLOCO
LARGURA_TOTAL = LARGURA_JOGO + LARGURA_PAINEL

tela = pygame.display.set_mode((LARGURA_TOTAL, ALTURA))
pygame.display.set_caption("Tetris em Python")
clock = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
CINZA = (40, 40, 40)
BRANCO = (255, 255, 255)
CORES = [
    (0, 255, 255),   # I
    (0, 0, 255),     # J
    (255, 165, 0),   # L
    (255, 255, 0),   # O
    (0, 255, 0),     # S
    (255, 0, 0),     # Z
    (128, 0, 128)    # T
]

# Formatos das peças
PECAS = [
    [[1, 1, 1, 1]],                         # I
    [[1, 0, 0], [1, 1, 1]],                # J
    [[0, 0, 1], [1, 1, 1]],                # L
    [[1, 1], [1, 1]],                      # O
    [[0, 1, 1], [1, 1, 0]],                # S
    [[1, 1, 0], [0, 1, 1]],                # Z
    [[0, 1, 0], [1, 1, 1]]                 # T
]

# Função: criar nova peça
def nova_peca():
    tipo = random.randint(0, len(PECAS) - 1)
    return {
        "forma": [linha[:] for linha in PECAS[tipo]],
        "x": COLUNAS // 2 - len(PECAS[tipo][0]) // 2,
        "y": 0,
        "cor": CORES[tipo]
    }

# Função: girar peça
def girar(peca):
    peca["forma"] = [list(l) for l in zip(*peca["forma"][::-1])]

# Função: detectar colisão
def colisao(tabuleiro, peca):
    for y, linha in enumerate(peca["forma"]):
        for x, bloco in enumerate(linha):
            if bloco:
                novo_x = peca["x"] + x
                novo_y = peca["y"] + y
                if novo_x < 0 or novo_x >= COLUNAS or novo_y >= LINHAS:
                    return True
                if novo_y >= 0 and tabuleiro[novo_y][novo_x] != PRETO:
                    return True
    return False

# Função: fixar peça no tabuleiro
def fixar(tabuleiro, peca):
    for y, linha in enumerate(peca["forma"]):
        for x, bloco in enumerate(linha):
            if bloco and 0 <= peca["y"] + y < LINHAS:
                tabuleiro[peca["y"] + y][peca["x"] + x] = peca["cor"]

# Função: remover linhas completas e retornar pontuação
def remover_linhas(tabuleiro):
    novas = [linha for linha in tabuleiro if PRETO in linha]
    linhas_removidas = LINHAS - len(novas)
    for _ in range(linhas_removidas):
        novas.insert(0, [PRETO] * COLUNAS)
    pontos = [0, 40, 100, 300, 1200][min(linhas_removidas, 4)]
    return novas, pontos

# Função: desenhar tabuleiro e painel lateral
def desenhar(tabuleiro, peca, proxima, pontuacao):
    tela.fill(CINZA)

    # Área do jogo
    for y in range(LINHAS):
        for x in range(COLUNAS):
            pygame.draw.rect(
                tela,
                tabuleiro[y][x],
                (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO, TAMANHO_BLOCO - 1, TAMANHO_BLOCO - 1)
            )

    # Peça atual
    for y, linha in enumerate(peca["forma"]):
        for x, bloco in enumerate(linha):
            if bloco:
                pygame.draw.rect(
                    tela,
                    peca["cor"],
                    ((peca["x"] + x) * TAMANHO_BLOCO,
                     (peca["y"] + y) * TAMANHO_BLOCO,
                     TAMANHO_BLOCO - 1, TAMANHO_BLOCO - 1)
                )

    # Painel lateral
    pygame.draw.rect(tela, (25, 25, 25), (LARGURA_JOGO, 0, LARGURA_PAINEL, ALTURA))
    fonte = pygame.font.SysFont("Arial", 24)
    texto = fonte.render("Pontuação:", True, BRANCO)
    tela.blit(texto, (LARGURA_JOGO + 20, 20))
    pontos_txt = fonte.render(str(pontuacao), True, BRANCO)
    tela.blit(pontos_txt, (LARGURA_JOGO + 40, 50))

    # Próxima peça
    texto2 = fonte.render("Próxima:", True, BRANCO)
    tela.blit(texto2, (LARGURA_JOGO + 20, 120))
    for y, linha in enumerate(proxima["forma"]):
        for x, bloco in enumerate(linha):
            if bloco:
                pygame.draw.rect(
                    tela,
                    proxima["cor"],
                    (LARGURA_JOGO + 50 + x * TAMANHO_BLOCO,
                     160 + y * TAMANHO_BLOCO,
                     TAMANHO_BLOCO - 2, TAMANHO_BLOCO - 2)
                )

    pygame.display.flip()

# Criação do tabuleiro
tabuleiro = [[PRETO for _ in range(COLUNAS)] for _ in range(LINHAS)]

peca_atual = nova_peca()
proxima_peca = nova_peca()
tempo_queda = 0
velocidade_queda = 5  # quanto menor, mais rápido
pontuacao = 0
rodando = True

# Loop principal
while rodando:
    clock.tick(30)
    tempo_queda += 1

    # Faz a peça cair
    if tempo_queda > velocidade_queda:
        peca_atual["y"] += 1
        if colisao(tabuleiro, peca_atual):
            peca_atual["y"] -= 1
            fixar(tabuleiro, peca_atual)
            tabuleiro, pontos = remover_linhas(tabuleiro)
            pontuacao += pontos
            peca_atual = proxima_peca
            proxima_peca = nova_peca()
            if colisao(tabuleiro, peca_atual):
                rodando = False
        tempo_queda = 0

    # Controles
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                peca_atual["x"] -= 1
                if colisao(tabuleiro, peca_atual):
                    peca_atual["x"] += 1
            elif evento.key == pygame.K_RIGHT:
                peca_atual["x"] += 1
                if colisao(tabuleiro, peca_atual):
                    peca_atual["x"] -= 1
            elif evento.key == pygame.K_DOWN:
                peca_atual["y"] += 1
                if colisao(tabuleiro, peca_atual):
                    peca_atual["y"] -= 1
            elif evento.key == pygame.K_UP:
                antiga = peca_atual["forma"]
                girar(peca_atual)
                if colisao(tabuleiro, peca_atual):
                    peca_atual["forma"] = antiga

    desenhar(tabuleiro, peca_atual, proxima_peca, pontuacao)

# Tela de fim de jogo
tela.fill(PRETO)
fonte = pygame.font.SysFont("Arial", 48)
texto_fim = fonte.render("GAME OVER", True, (255, 0, 0))
tela.blit(texto_fim, (LARGURA_JOGO // 2 - 120, ALTURA // 2 - 50))
pygame.display.flip()
pygame.time.wait(2500)
pygame.quit()
