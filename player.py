import pygame
from settings import *
from weapons import Bala

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_balas):
        super().__init__()
        self.grupo_balas = grupo_balas # Recebe o grupo de balas para atirar corretamente
        self.velocidade = pygame.Vector2(0, 0)
        self.aceleracao = pygame.Vector2(0.2, 0.2)
        self.friccao = pygame.Vector2(0.1, 0.1)
        self.imagens = {
            'esquerda': pygame.image.load('player_esquerda.png').convert_alpha(),
            'direita': pygame.image.load('player_direita.png').convert_alpha(),
            'cima': pygame.image.load('player_cima.png').convert_alpha(),
            'baixo': pygame.image.load('player_baixo.png').convert_alpha(),
            'soco_cima': pygame.image.load('player_soco_cima.png').convert_alpha(),
            'soco_baixo': pygame.image.load('player_soco_baixo.png').convert_alpha(),
            'soco_esquerda': pygame.image.load('player_soco_esquerda.png').convert_alpha(),
            'soco_direita': pygame.image.load('player_soco_direita.png').convert_alpha(),
            'fuzil_cima': pygame.image.load('player_fuzil_cima.png').convert_alpha(),
            'fuzil_baixo': pygame.image.load('player_fuzil_baixo.png').convert_alpha(),
            'fuzil_esquerda': pygame.image.load('player_fuzil_esquerda.png').convert_alpha(),
            'fuzil_direita': pygame.image.load('player_fuzil_direita.png').convert_alpha(),
            'tiro_baixo': pygame.image.load('player_tiro_baixo.png').convert_alpha(),
            'tiro_cima': pygame.image.load('player_tiro_cima.png').convert_alpha(),
            'tiro_esquerda': pygame.image.load('player_tiro_esquerda.png').convert_alpha(),
            'tiro_direita': pygame.image.load('player_tiro_direita.png').convert_alpha(),
        }
        
        self.imagem_atual = self.imagens['baixo']
        self.rect = self.imagem_atual.get_rect()
        self.rect.center = (x, y)
        self.velocidade = pygame.Vector2(0, 0)
        self.arma_selecionada = 'soco'
        self.socando = False
        self.tempo_soco = 0
        self.duracao_soco = 20
        self.coletou_fuzil = False
        self.direcao_atual = 'baixo'
        self.balas_fuzil = 0
        self.sem_municao = False
        self.balas_coletadas = 0
        self.mouse_pressed_previous = False
         
    def atirar(self):
        if self.arma_selecionada == 'fuzil' and self.balas_fuzil > 0 and not self.sem_municao:
            self.balas_fuzil -= 1
            nova_bala = Bala(self.rect.center, self.direcao_atual)
            self.grupo_balas.add(nova_bala)
            self.imagem_atual = self.imagens[f'tiro_{self.direcao_atual}']
            self.sem_municao = True
            return 
    
    def recarregar_fuzil(self):
        if self.balas_fuzil == 0 and self.balas_coletadas > 0:
            self.balas_fuzil = 60 
            self.balas_coletadas -= 1
            self.imagem_atual = self.imagens[f'fuzil_{self.direcao_atual}']

    def soltar_fuzil(self):
        self.coletou_fuzil = False
        self.arma_selecionada = 'soco'
        self.imagem_atual = self.imagens[self.direcao_atual]
     
    def update(self):
        mouse_pressed_current = pygame.mouse.get_pressed()[0]  
        
        if not mouse_pressed_current and self.mouse_pressed_previous:
            self.atirar()
        
        self.mouse_pressed_previous = mouse_pressed_current  
        aceleracao = pygame.Vector2(0, 0)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            aceleracao.x = -0.2
            self.direcao_atual = 'esquerda'
        if teclas[pygame.K_d]:
            aceleracao.x = 0.2
            self.direcao_atual = 'direita'
        if teclas[pygame.K_w]:
            aceleracao.y = -0.2
            self.direcao_atual = 'cima'
        if teclas[pygame.K_s]:
            aceleracao.y = 0.2
            self.direcao_atual = 'baixo'
        
        self.velocidade.x += aceleracao.x
        self.velocidade.x = min(max(-5, self.velocidade.x), 5)
        self.velocidade.y += aceleracao.y
        self.velocidade.y = min(max(-5, self.velocidade.y), 5)
        self.rect.move_ip(self.velocidade.x, self.velocidade.y)

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(LARGURA_JANELA, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(ALTURA_JANELA, self.rect.bottom)

        if pygame.mouse.get_pressed()[0]:
            self.atirar()

        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.socando:
            self.socar()

        if not self.socando:
            if self.arma_selecionada == 'fuzil':
                if pygame.mouse.get_pressed()[0]:
                    self.imagem_atual = self.imagens[f'tiro_{self.direcao_atual}']
                else:
                    self.imagem_atual = self.imagens[f'fuzil_{self.direcao_atual}']
            else:
                if self.direcao_atual in self.imagens:
                    self.imagem_atual = self.imagens[self.direcao_atual]

        if self.socando:
            self.tempo_soco += 1
            if self.tempo_soco >= self.duracao_soco:
                self.socando = False
                self.tempo_soco = 0
                self.imagem_atual = self.imagens[self.direcao_atual]

        self.rect.x = max(0, min(self.rect.x, LARGURA_JANELA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTURA_JANELA - self.rect.height))
 
    def socar(self):
        if self.arma_selecionada == 'soco':
            self.socando = True
            if self.imagem_atual == self.imagens['cima']:
                self.imagem_atual = self.imagens['soco_cima']
            elif self.imagem_atual == self.imagens['baixo']:
                self.imagem_atual = self.imagens['soco_baixo']
            elif self.imagem_atual == self.imagens['esquerda']:
                self.imagem_atual = self.imagens['soco_esquerda']
            elif self.imagem_atual == self.imagens['direita']:
                self.imagem_atual = self.imagens['soco_direita']   

        if self.socando:
            self.tempo_soco += 1
            if self.tempo_soco >= self.duracao_soco:
                self.socando = False
                self.tempo_soco = 0
                self.imagem_atual = self.imagens[self.direcao_atual]