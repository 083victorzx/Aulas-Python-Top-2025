import pygame
import subprocess
import sys

pygame.init()

# --- TELA CHEIA ---
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
larg, alt = tela.get_size()

pygame.display.set_caption("Menu de Jogos")

fonte = pygame.font.Font(None, 60)
clock = pygame.time.Clock()

# Lista dos jogos + sair
jogos = [
    ("Jogo de Desviar V1", "jogo_desviarV1.py"),
    ("Jogo de Desviar V2", "jogo_desviarV2.py"),
    ("Ping Pong", "jogo_ping_pong.py"),
    ("Undertale Fight", "jogo_undertale.py"),
    ("Tetris", "jogo_tetris.py"),
    ("Cobrinha", "jogo_cobrinha.py"),
    ("Sair do Jogo", None)  # Nova opção!
]

opcao = 0  # índice selecionado


def desenhar_menu():
    tela.fill((0, 0, 0))

    titulo = fonte.render("MENU PRINCIPAL", True, (255, 255, 255))
    tela.blit(titulo, (larg // 2 - titulo.get_width() // 2, 80))

    for i, (nome, _) in enumerate(jogos):
        cor = (255, 255, 0) if i == opcao else (255, 255, 255)
        texto = fonte.render(nome, True, cor)
        tela.blit(texto, (larg // 2 - texto.get_width() // 2, 200 + i * 70))

    pygame.display.update()


def executar_jogo(arquivo):
    if arquivo is None:
        pygame.quit()
        sys.exit()

    subprocess.call([sys.executable, arquivo])  # roda e espera terminar


# --- LOOP PRINCIPAL ---
rodando = True
while rodando:
    desenhar_menu()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            # Fechar com ESC
            if evento.key == pygame.K_ESCAPE:
                rodando = False

            if evento.key == pygame.K_UP:
                opcao = (opcao - 1) % len(jogos)

            elif evento.key == pygame.K_DOWN:
                opcao = (opcao + 1) % len(jogos)

            elif evento.key == pygame.K_RETURN:  # ENTER
                nome, arquivo = jogos[opcao]
                executar_jogo(arquivo)

pygame.quit()
