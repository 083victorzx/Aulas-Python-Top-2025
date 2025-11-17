import pygame
import random
import math

pygame.init()
pygame.mixer.init()

# -------- CONFIGURAÇÕES -----------
LARGURA_TELA, ALTURA_TELA = 1440, 900
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
clock = pygame.time.Clock()
pygame.display.set_caption("Desviar - Estilo Undertale")

# Caixa de combate
COMB_LARG, COMB_ALT = 900, 560
comb_rect = pygame.Rect(
    (LARGURA_TELA - COMB_LARG) // 2,
    (ALTURA_TELA - COMB_ALT) // 2,
    COMB_LARG,
    COMB_ALT
)

# Fonte
def load_pixel_font(size):
    for nome in ["Determination Mono", "DeterminationSans", "PressStart2P", "Courier New", "monospace"]:
        try:
            return pygame.font.SysFont(nome, size)
        except:
            continue
    return pygame.font.Font(None, size)

fonte_titulo = load_pixel_font(64)
fonte_sub = load_pixel_font(24)

# Função para desenhar coração pixelado
def desenhar_coracao_pixel(surface, cx, cy, tamanho, cor):
    mapa = [
        " 11 11 ",
        "1111111",
        "1111111",
        " 11111 ",
        "  111  ",
        "   1   "
    ]
    pixel = tamanho // 6
    if pixel < 2: pixel = 2
    ox = cx - (len(mapa[0]) * pixel) // 2
    oy = cy - (len(mapa) * pixel) // 2
    for ry, linha in enumerate(mapa):
        for rx, ch in enumerate(linha):
            if ch == "1":
                pygame.draw.rect(surface, cor, (ox + rx*pixel, oy + ry*pixel, pixel, pixel))

# Funções auxiliares
def clamp_soul(x, y):
    half = SOUL_SIZE
    return (
        max(comb_rect.left + half, min(comb_rect.right - half, x)),
        max(comb_rect.top + half, min(comb_rect.bottom - half, y))
    )

def criar_obstaculo():
    tamanho_obst = 20  # tamanho dos obstáculos
    side = random.choice(["top","left","right","bottom"])
    speed = velocidade_obstaculos + random.random() * 1.2
    pad = 8
    if side == "top":
        x = random.randint(comb_rect.left + pad, comb_rect.right - tamanho_obst - pad)
        y = comb_rect.top - tamanho_obst - 10
        return pygame.Rect(x, y, tamanho_obst, tamanho_obst), 0, speed
    if side == "bottom":
        x = random.randint(comb_rect.left + pad, comb_rect.right - tamanho_obst - pad)
        y = comb_rect.bottom + 10
        return pygame.Rect(x, y, tamanho_obst, tamanho_obst), 0, -speed
    if side == "left":
        x = comb_rect.left - tamanho_obst - 10
        y = random.randint(comb_rect.top + pad, comb_rect.bottom - tamanho_obst - pad)
        return pygame.Rect(x, y, tamanho_obst, tamanho_obst), speed, 0
    x = comb_rect.right + 10
    y = random.randint(comb_rect.top + pad, comb_rect.bottom - tamanho_obst - pad)
    return pygame.Rect(x, y, tamanho_obst, tamanho_obst), -speed, 0

# -------- LOOP PRINCIPAL DO JOGO -----------
def jogar():
    global SOUL_SIZE, velocidade_jogador, velocidade_obstaculos, freq_obstaculos

    SOUL_SIZE = 18
    soul_x = comb_rect.centerx
    soul_y = comb_rect.centery
    velocidade_jogador = 5.0
    velocidade_obstaculos = 4.5
    freq_obstaculos = 100
    tamanho_obst = 36
    obstaculos = []
    inicio = pygame.time.get_ticks()
    ultima_fase = 0
    duracao_fase = 0.25
    cores_fases = [(0,0,0), (30,30,30), (10,10,10), (40,0,0), (0,30,40)]
    cor_fundo = (0, 0, 0)
    pausado = False
    fade_pausado = 0.0
    rodando = True
    tempo_morte = None

    while rodando:
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - inicio) / 1000.0

        fase_atual = int(tempo_decorrido // duracao_fase)
        if fase_atual > ultima_fase:
            ultima_fase = fase_atual
            velocidade_obstaculos += 0.25
            velocidade_jogador += 0.12
            freq_obstaculos = max(6, freq_obstaculos - 4)
            cor_fundo = cores_fases[fase_atual % len(cores_fases)]

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if not pausado:
                        pausado = True
                        fade_pausado = 0.0
                    else:
                        return False
                elif pausado and (evento.key == pygame.K_SPACE or evento.key == pygame.K_RETURN):
                    pausado = False
                    fade_pausado = 0.0

        if pausado:
            fade_pausado = min(255, fade_pausado + 6.0)
            tela.fill(cor_fundo)
            pygame.draw.rect(tela, (255,255,255), comb_rect, 8)
            desenhar_coracao_pixel(tela, soul_x, soul_y, SOUL_SIZE, (255,255,255))
            texto_surf = fonte_titulo.render("JOGO PAUSADO", True, (255,255,255))
            sub_surf = fonte_sub.render("Pressione ESPAÇO ou ENTER para continuar", True, (200,200,200))
            tela.blit(texto_surf, (LARGURA_TELA//2 - texto_surf.get_width()//2, comb_rect.top + 40))
            tela.blit(sub_surf, (LARGURA_TELA//2 - sub_surf.get_width()//2, comb_rect.top + 110))
            pygame.display.flip()
            clock.tick(60)
            continue

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: soul_x -= velocidade_jogador
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: soul_x += velocidade_jogador
        if teclas[pygame.K_UP] or teclas[pygame.K_w]: soul_y -= velocidade_jogador
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: soul_y += velocidade_jogador
        soul_x, soul_y = clamp_soul(soul_x, soul_y)

        if random.randint(1, freq_obstaculos) == 1:
            obst, vx, vy = criar_obstaculo()
            obstaculos.append((obst, vx, vy))

        tela.fill(cor_fundo)
        pygame.draw.rect(tela, (255,255,255), comb_rect, 8)
        inner = comb_rect.inflate(-16, -16)
        pygame.draw.rect(tela, (0,0,0), inner)
        desenhar_coracao_pixel(tela, soul_x, soul_y, SOUL_SIZE, (255,255,255))

        novos = []
        soul_rect = pygame.Rect(0, 0, SOUL_SIZE, SOUL_SIZE)
        soul_rect.center = (soul_x, soul_y)
        for (obst, vx, vy) in obstaculos:
            obst.x += vx
            obst.y += vy
            pygame.draw.rect(tela, (255,255,255), obst)
            pygame.draw.rect(tela, (180,20,20), obst.inflate(-6, -6))
            if obst.colliderect(soul_rect) and comb_rect.colliderect(obst):
                tempo_morte = tempo_decorrido
                rodando = False
            margem = 80
            if (comb_rect.left - margem <= obst.x <= comb_rect.right + margem) and (comb_rect.top - margem <= obst.y <= comb_rect.bottom + margem):
                novos.append((obst, vx, vy))
        obstaculos = novos

        tempo_txt = fonte_sub.render(f"Tempo: {tempo_decorrido:.2f}s", True, (255,255,255))
        tela.blit(tempo_txt, (LARGURA_TELA - tempo_txt.get_width() - 20, 20))

        msg = fonte_sub.render("Use ← ↑ ↓ → (ou WASD) para mover. ESC pausa.", True, (200,200,200))
        tela.blit(msg, (comb_rect.left + 12, comb_rect.bottom + 12))

        pygame.display.flip()
        clock.tick(60)

    # Tela final
    while True:
        tela.fill((0,0,0))
        fim_txt = fonte_titulo.render("VOCÊ PERDEU!", True, (255,255,255))
        tempo_txt = fonte_sub.render(f"Você sobreviveu por {tempo_morte:.2f} segundos.", True, (200,200,200))
        retry_txt = fonte_sub.render("Pressione ENTER para tentar novamente ou ESC para sair.", True, (180,180,180))
        tela.blit(fim_txt, (LARGURA_TELA//2 - fim_txt.get_width()//2, ALTURA_TELA//2 - 80))
        tela.blit(tempo_txt, (LARGURA_TELA//2 - tempo_txt.get_width()//2, ALTURA_TELA//2))
        tela.blit(retry_txt, (LARGURA_TELA//2 - retry_txt.get_width()//2, ALTURA_TELA//2 + 60))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False
        clock.tick(60)

# -------- INÍCIO --------
while True:
    if not jogar():
        break

pygame.quit()