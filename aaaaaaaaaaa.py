import pygame
import sys
import random
from settings import *
from weapons import Fuzil, Bala, Pente
from player import Player

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption(TITULO_JANELA)
clock = pygame.time.Clock()
imagem_fundo = pygame.image.load('fundo2.jpg')

# Criando grupos primeiro
fuzis = pygame.sprite.Group()
balas = pygame.sprite.Group()
pentes = pygame.sprite.Group()

# Criando o player (e passando o grupo de balas para ele)
player = Player(LARGURA_MAPA // 2, ALTURA_MAPA // 2, balas)

posicoes_fuzis = []
for _ in range(20):
    x = random.randint(0, LARGURA_MAPA)
    y = random.randint(0, ALTURA_MAPA)
    while (x, y) in posicoes_fuzis:
        x = random.randint(0, LARGURA_MAPA)
        y = random.randint(0, ALTURA_MAPA)
    fuzil = Fuzil(x, y)
    fuzis.add(fuzil)
    posicoes_fuzis.append((x, y))

posicoes_pentes = []
for _ in range(80):
    x = random.randint(0, LARGURA_MAPA)
    y = random.randint(0, ALTURA_MAPA)
    while (x, y) in posicoes_pentes:
        x = random.randint(0, LARGURA_MAPA)
        y = random.randint(0, ALTURA_MAPA)
    pente = Pente(x, y)
    pentes.add(pente)
    posicoes_pentes.append((x, y))

jogando = True
tempo_entre_disparos = 0 

# Loop principal
while jogando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                player.arma_selecionada = 'soco' 
            elif evento.key == pygame.K_DOWN and player.coletou_fuzil:
                player.arma_selecionada = 'fuzil' 
            elif evento.key == pygame.K_f:
                if not player.coletou_fuzil:
                    colisoes_fuzis = pygame.sprite.spritecollide(player, fuzis, False)
                    for fuzil in colisoes_fuzis:
                        if pygame.sprite.collide_rect(player, fuzil):
                            player.coletou_fuzil = True
                            fuzil.kill() 
                            player.imagem_atual = player.imagens[f'fuzil_{player.direcao_atual}']
                            player.balas_fuzil = 15 
                else:
                    player.soltar_fuzil() 
                    novo_fuzil = Fuzil(player.rect.x, player.rect.y)
                    fuzis.add(novo_fuzil)
            elif evento.key == pygame.K_r:
                player.recarregar_fuzil()
                player.balas_fuzil += 60 
            elif evento.key == pygame.K_c:
                colisoes_pentes = pygame.sprite.spritecollide(player, pentes, True)
                player.balas_coletadas += len(colisoes_pentes) # Adiciona a quantidade de pentes coletados
            
    player.update()

    if pygame.mouse.get_pressed()[0] and tempo_entre_disparos == 0:
        player.atirar()
        tempo_entre_disparos = 62

    if tempo_entre_disparos > 0:
       tempo_entre_disparos -= 1

    if not pygame.mouse.get_pressed()[0]:
        player.sem_municao = False
    
    balas.update()

    # Renderização
    tela.blit(imagem_fundo, (0, 0))
    tela.blit(player.imagem_atual, player.rect)

    for fuzil in fuzis:
        fuzil.draw(tela)
    for pente in pentes:
        pente.draw(tela)
    for bala in balas:
        tela.blit(bala.image, bala.rect)

    # Textos da UI
    fonte = pygame.font.Font(None, 36)
    texto_arma_selecionada = fonte.render('Arma: ' + player.arma_selecionada.capitalize(), True, BRANCO)
    tela.blit(texto_arma_selecionada, (10, 10))

    if player.arma_selecionada == 'fuzil':
        texto_balas = fonte.render('Balas: ' + str(player.balas_fuzil), True, BRANCO)
        tela.blit(texto_balas, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)
    
    if not pygame.mouse.get_pressed()[0]:
        player.sem_municao = False

pygame.quit()
sys.exit()