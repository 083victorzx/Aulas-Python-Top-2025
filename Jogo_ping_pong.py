import pygame
import random
import time
display_h, display_w = 600, 1200
tela = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Jogo de Ping Pong')

pygame.init()

jogador_w, jogador_h = 20, 150
jogador = pygame.Rect(20, 0, jogador_w, jogador_h)
jogador_2_w, jogador_2_h = 20, 150
jogador_2 = pygame.Rect(display_w - 20 - jogador_2_w , 0, jogador_2_w, jogador_2_h)


bola = pygame.Rect((display_w/2)-10, (display_h/2)-10, 20, 20)
clock = pygame.time.Clock()

obstaculos = []

# velocidade em cada eixo da bola
speed_x = 15
speed_y = 5


freq_obs = 300 # frequencia de obstaculos


# "corações" de vida e também a borda que fica ao redor da barra de vida
vidas = [
    pygame.Rect(200, 40, 70, 25),
    pygame.Rect(270, 40, 70, 25),
    pygame.Rect(340, 40, 70, 25),
]
bordas_vidas = [
    pygame.Rect(200, 40, 70, 25),
    pygame.Rect(270, 40, 70, 25),
    pygame.Rect(340, 40, 70, 25),
]





running = True
# geração de  obstaculos dentro de um limite e impede que a quantidade de obstaculos passe de 3
def gerar_obs():
    if random.randint(0, freq_obs) == 1 and len(obstaculos) < 3:
        return obstaculos.append(pygame.Rect(100+(random.randint(0, display_w - 240)), 50+(50 + random.randint(0, display_h - 140)), 40, 40))
def limpa_geral():
    global speed_x, speed_y, vidas
    obstaculos.clear()
    speed_x = 15
    speed_y = 5
    bola.x = (display_w/2)-10
    bola.y = (display_h/2)-10
    jogador.y = 0
    jogador_2.y = 0
    vidas = [
    pygame.Rect(200, 40, 70, 25),
    pygame.Rect(270, 40, 70, 25),
    pygame.Rect(340, 40, 70, 25),
    ]

def tela_gameover():
    while True:
            tela.fill((0,0,0))
            borda = pygame.Rect(display_w/2 - 300, display_h/2 - 150, 600, 300)
            pygame.draw.rect(tela, (255,255,255), borda, 2)
            tela.blit(texto_over, (display_w/2 - over_x/2, display_h/2 - over_y/2 - 20))
            tela.blit(texto_reiniciar, (display_w/2 - reiniciar_x/2 + 100 , display_h/2 - reiniciar_y/2 + 40))
            tela.blit(texto_sair, (display_w/2 - sair_x/2 - 100, display_h/2 - sair_y/2 + 40))

            evento = pygame.event.get()
            for e in evento:
                if e.type == pygame.QUIT:
                    return "x"
                    break
            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_r]:
                return "r"
                break
            if tecla[pygame.K_x]:
                return "x"
                break
            pygame.display.update()

while running:
    # chama a função que gera obstaculos aleatórios
    gerar_obs()
    # evento de saída
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fontes e textos da tela do game over

    fonte_over = pygame.font.Font(None, 70)
    texto_over = fonte_over.render("Game Over", True, (255,255,255))
    over_x, over_y = texto_over.get_size()

    fonte_reiniciar = pygame.font.Font(None, 25)
    texto_reiniciar = fonte_reiniciar.render("Aperte R para reiniciar", True, (255,255,255))
    reiniciar_x, reiniciar_y = texto_reiniciar.get_size()

    fonte_sair = pygame.font.Font(None, 25)
    texto_sair = fonte_sair.render("Aperte X para sair", True, (255,255,255))
    sair_x, sair_y = texto_sair.get_size()

    
    # termina o jogo se a quantidade de vida chegar a zero
    if len(vidas) <= 0:
        escolha = tela_gameover()
        match(escolha):
            case "r":
                limpa_geral()
            case "x":
                running = False
                break

    # controle do jogador 1
    key = pygame.key.get_pressed()

    # mover para cima
    if (key[pygame.K_w] or key[pygame.K_UP]) and jogador.y > 0:
        jogador.y -= 10

    # mover para baixo
    if (key[pygame.K_s] or key[pygame.K_DOWN]) and jogador.y < display_h - jogador_h:
        jogador.y += 10


    # impede que a bola passe dos limites da tela
    if bola.y >= display_h - 20:
        speed_y *= -1
    elif bola.y <= 0:
        speed_y *= -1
    
    # colisões da bola
    if bola.colliderect(jogador_2):
        speed_x *= -1.05
        speed_y *= 1.05

    elif bola.colliderect(jogador):
        speed_x *= -1.05
        speed_y *= 1.05
    # mantém a bola em constante movimentação
    bola.y += speed_y
    bola.x += speed_x

    # posição do jogador 2(ele segue a bola)
    jogador_2.y = (bola.y - jogador_2_h/2) + 10

    #Ponto player 1
    if bola.x >= display_w - 20:
        bola.x = (display_w/2)-10
        bola.y = (display_h/2)-10
        speed_y = 5
        speed_x = 15
    #Ponto player 2
    elif bola.x <= 0:
        vidas.pop()
        bola.x = (display_w/2)-10
        bola.y = (display_h/2)-10
        speed_y = 5
        speed_x = 15

    # fonte e texto

    # impede que o jogador 2 saia dos limites da tela
    if jogador_2.y <0:
        jogador_2.y = 0
    elif jogador_2.y > display_h - jogador_2_h:
        jogador_2.y = display_h - jogador_2_h
    #colisões dos obstaculos com a bola
    for obs in obstaculos:
        if bola.colliderect(obs):
            obstaculos.remove(obs)
            speed_y *= -1




    tela.fill((0,0,0))



    # renderização de tudo
    for v in vidas:
        pygame.draw.rect(tela, (255,0,0), v)
    for vb in bordas_vidas:
        pygame.draw.rect(tela, (150, 0, 0), vb, 2)
    # mostra o texto
    # renderiza os elementos principais
    pygame.draw.rect(tela, (0, 255, 100), jogador)
    pygame.draw.rect(tela, (255,160,0), jogador_2)
    pygame.draw.rect(tela, (100,170,200), bola)
    # renderiza os obstaculos
    for obs in obstaculos:
        pygame.draw.rect(tela, (255,255,255), obs, 3)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()