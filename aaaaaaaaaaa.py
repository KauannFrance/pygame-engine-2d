import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da janela
LARGURA_JANELA = 1600
ALTURA_JANELA = 900
TITULO_JANELA = 'Meu Jogo'
FPS = 60


# Definindo a janela e o modo de vídeo
tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption(TITULO_JANELA)
# Criando o objeto Clock
clock = pygame.time.Clock()
# Tamanho do mapa
LARGURA_MAPA = 1600
ALTURA_MAPA = 900

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# Carregar a imagem de fundo
imagem_fundo = pygame.image.load('fundo2.jpg')



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.velocidade = pygame.Vector2(0, 0)
        self.aceleracao = pygame.Vector2(0.2, 0.2)  # Ajuste a aceleração conforme necessário
        self.friccao = pygame.Vector2(0.1, 0.1)  # Ajuste a fricção conforme necessário
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
        self.velocidade = pygame.Vector2(0, 0)  # Inicializando como vetor
        self.arma_selecionada = 'soco'  # Inicialmente seleciona o soco como arma
        self.socando = False
        self.tempo_soco = 0
        self.duracao_soco = 20  # Duração do soco em ticks
        self.coletou_fuzil = False
        self.direcao_atual = 'baixo'  # Armazena a direção atual
        self.balas_fuzil = 0  # Contador de balas de fuzil
        self.sem_municao = False  # Flag para indicar que o jogador está sem munição
        self.balas_coletadas = 0  # Contador de balas coletadas
        self.mouse_pressed_previous = False  # Variável para rastrear o estado anterior do botão do mouse
         

    def atirar(self):
        if self.arma_selecionada == 'fuzil' and self.balas_fuzil > 0 and tempo_entre_disparos == 0 and not self.sem_municao:
            self.balas_fuzil -= 1
            nova_bala = Bala(self.rect.center, self.direcao_atual)
            balas.add(nova_bala)
            self.imagem_atual = self.imagens[f'tiro_{self.direcao_atual}']
            self.sem_municao = True  # Define a flag como verdadeira para impedir disparos contínuos
            return  # Sai da função após disparar uma bala
        # Verifica se o botão do mouse foi pressionado e depois solto
       

    
    def recarregar_fuzil(self):
        if self.balas_fuzil == 0 and self.balas_coletadas > 0:
            self.balas_fuzil = 60  # Corrigindo para 60 balas por pente
            self.balas_coletadas -= 1

            # Atualiza a imagem do jogador para segurar o fuzil recarregado
            self.imagem_atual = self.imagens[f'fuzil_{self.direcao_atual}']
     
    def update(self):
        # Verifica o estado atual do botão do mouse
        mouse_pressed_current = pygame.mouse.get_pressed()[0]  
        
        # Verifica se o botão do mouse foi pressionado e depois solto
        if not mouse_pressed_current and self.mouse_pressed_previous:
            self.atirar()
        
        # Atualiza o estado anterior do botão do mouse
        self.mouse_pressed_previous = mouse_pressed_current  
        # Define a aceleração com base nas teclas pressionadas
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

        
        # Adiciona a aceleração à velocidade (componente x)
        self.velocidade.x += aceleracao.x

        # Limita a velocidade máxima (componente x)
        self.velocidade.x = min(max(-5, self.velocidade.x), 5)

        # Adiciona a aceleração à velocidade (componente y)
        self.velocidade.y += aceleracao.y

        # Limita a velocidade máxima (componente y)
        self.velocidade.y = min(max(-5, self.velocidade.y), 5)

        # Move o jogador com base na velocidade
        self.rect.move_ip(self.velocidade.x, self.velocidade.y)

        # Mantém o jogador dentro dos limites da tela
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(LARGURA_JANELA, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(ALTURA_JANELA, self.rect.bottom)

        # Verifica se o jogador está atirando
        if pygame.mouse.get_pressed()[0]:
            self.atirar()

        # Verifica se o jogador está socando
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.socando:
            self.socar()

        # Atualiza a imagem do jogador
        if not self.socando:
            if self.arma_selecionada == 'fuzil':
                if pygame.mouse.get_pressed()[0]:
                    self.imagem_atual = self.imagens[f'tiro_{self.direcao_atual}']
                else:
                    self.imagem_atual = self.imagens[f'fuzil_{self.direcao_atual}']
            else:
                if self.direcao_atual in self.imagens:
                    self.imagem_atual = self.imagens[self.direcao_atual]

        # Verifica se o jogador está socando e atualiza o tempo de soco
        if self.socando:
            self.tempo_soco += 1
            if self.tempo_soco >= self.duracao_soco:
                self.socando = False
                self.tempo_soco = 0
                # Retorna a imagem para a direção anterior
                self.imagem_atual = self.imagens[self.direcao_atual]

        # Limita o movimento do jogador dentro dos limites da janela
        self.rect.x = max(0, min(self.rect.x, LARGURA_JANELA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTURA_JANELA - self.rect.height))
 
    def socar(self):
            if self.arma_selecionada == 'soco':
                self.socando = True
                # Atualiza a imagem para a do soco na direção atual
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
                    # Retorna a imagem para a direção anterior
                    self.imagem_atual = self.imagens[self.direcao_atual]   


class Fuzil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imagem = pygame.image.load('fuzil.png').convert_alpha()
        self.rect = self.imagem.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.balas = 15
    def draw(self, surface):
        surface.blit(self.imagem, self.rect)


class Bala(pygame.sprite.Sprite):
    def __init__(self, posicao, direcao):
        super().__init__()
        self.image = pygame.image.load('bala.png').convert_alpha()
        self.rect = self.image.get_rect(center=posicao)
        self.direction = direcao
        self.speed = 10  # Aumentei a velocidade da bala para 10 pixels por atualização
        # Carregar efeito sonoro de disparo
        self.sound_disparo = pygame.mixer.Sound('tiro_espin.mp3')
        self.sound_disparo.set_volume(0.5)  # Ajuste o volume conforme necessário
        self.som_disparado = False  # Flag para controlar se o som já foi reproduzido ou não
    def update(self):
        # Movimento da bala com base na direção
        if self.direction == 'esquerda':
            self.rect.x -= self.speed
        elif self.direction == 'direita':
            self.rect.x += self.speed
        elif self.direction == 'cima':
            self.rect.y -= self.speed
        elif self.direction == 'baixo':
            self.rect.y += self.speed

         # Reproduzir o som de disparo apenas uma vez quando a bala é criada
        if not self.som_disparado:
            self.sound_disparo.play()
            self.som_disparado = True  # Define a flag como True para indicar que o som já foi reproduzido

    def draw(self, surface):
        surface.blit(self.image, self.rect)
      

class Pente(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imagem = pygame.image.load('pente_fuzil.png').convert_alpha()
        self.rect = self.imagem.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.imagem, self.rect)


# Criando o player
player = Player(LARGURA_MAPA // 2, ALTURA_MAPA // 2)

# Criando grupos para fuzis, balas e pentes de balas
fuzis = pygame.sprite.Group()
balas = pygame.sprite.Group()
pentes = pygame.sprite.Group()

# Lista para armazenar as posições das armas já geradas
posicoes_fuzis = []
# Criando fuzis aleatórios pelo mapa
for _ in range(20):
    x = random.randint(0, LARGURA_MAPA)
    y = random.randint(0, ALTURA_MAPA)
    # Verifica se a posição gerada já foi utilizada por outra arma
    while (x, y) in posicoes_fuzis:
        x = random.randint(0, LARGURA_MAPA)
        y = random.randint(0, ALTURA_MAPA)
    fuzil = Fuzil(x, y)
    fuzis.add(fuzil)
    posicoes_fuzis.append((x, y))

# Lista para armazenar as posições dos pentes de balas já gerados
posicoes_pentes = []
# Criando pentes de balas aleatórios pelo mapa
for _ in range(80):
    x = random.randint(0, LARGURA_MAPA)
    y = random.randint(0, ALTURA_MAPA)
    # Verifica se a posição gerada já foi utilizada por outro pente
    while (x, y) in posicoes_pentes:
     x = random.randint(0, LARGURA_MAPA)
     y = random.randint(0, ALTURA_MAPA)
    pente = Pente(x, y)
    pentes.add(pente)
    posicoes_pentes.append((x, y))

jogando = True
tempo_entre_disparos = 0  # Definindo a variável corretamente

# Loop principal do jogo
while jogando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
        elif evento.type == pygame.KEYDOWN:
            # Lógica para lidar com eventos de teclado
            if evento.key == pygame.K_UP:
                player.arma_selecionada = 'soco'  # Escolhe soco
            elif evento.key == pygame.K_DOWN and player.coletou_fuzil:
                player.arma_selecionada = 'fuzil'  # Escolhe fuzil
            elif evento.key == pygame.K_f:
                # Coletar ou soltar o fuzil
                if not player.coletou_fuzil:
                    colisoes_fuzis = pygame.sprite.spritecollide(player, fuzis, False)
                    for fuzil in colisoes_fuzis:
                        if pygame.sprite.collide_rect(player, fuzil):
                            player.coletou_fuzil = True
                            fuzil.kill()  # Remove o fuzil do grupo
                            # Atualiza a imagem do jogador para segurar o fuzil
                            player.imagem_atual = player.imagens[f'fuzil_{player.direcao_atual}']
                            player.balas_fuzil = 15  # Define o contador de balas para 15
                else:
                    player.soltar_fuzil()  # Solta o fuzil
                    # Solta o fuzil na posição do jogador
                    novo_fuzil = Fuzil(player.rect.x, player.rect.y)
                    fuzis.add(novo_fuzil)
            elif evento.key == pygame.K_r:
                # Recarregar o fuzil
                player.recarregar_fuzil()
                player.balas_fuzil += 60  # Adiciona 60 balas ao contador do fuzil
            elif evento.key == pygame.K_c:
                # Coletar pentes de balas
                colisoes_pentes = pygame.sprite.spritecollide(player, pentes, True)
            

    # Atualização do player
    player.update()

    # Controle de disparo com tempo entre os disparos
    if pygame.mouse.get_pressed()[0] and tempo_entre_disparos == 0:
        player.atirar()
        # Define o tempo entre os disparos como 180 ticks (3 segundos a 60 FPS)
        tempo_entre_disparos = 62

    # Subtrai 1 do tempo entre os disparos em cada ciclo do loop
    if tempo_entre_disparos > 0:
       tempo_entre_disparos -= 1

    if not pygame.mouse.get_pressed()[0]:
        player.sem_municao = False
    
    # Atualização das balas
    balas.update()

    # Renderização
     #Desenhar a imagem de fundo na tela
    tela.blit(imagem_fundo, (0, 0))

    tela.blit(player.imagem_atual, player.rect)

    # Desenha os fuzis
    for fuzil in fuzis:
        fuzil.draw(tela)

    # Desenha os pentes de balas
    for pente in pentes:
        pente.draw(tela)

    # Desenha as balas
    for bala in balas:
        tela.blit(bala.image, bala.rect)

    # Exibir texto com a arma selecionada
    fonte = pygame.font.Font(None, 36)
    texto_arma_selecionada = fonte.render('Arma: ' + player.arma_selecionada.capitalize(), True, BRANCO)
    tela.blit(texto_arma_selecionada, (10, 10))

    # Exibir contador de balas
    if player.arma_selecionada == 'fuzil':
        texto_balas = fonte.render('Balas: ' + str(player.balas_fuzil), True, BRANCO)
        tela.blit(texto_balas, (10, 50))

    # Atualização da tela
    pygame.display.flip()
    clock.tick(FPS)
    
    # Reset da flag sem_municao quando o jogador parar de atirar
if not pygame.mouse.get_pressed()[0]:
    player.sem_municao = False

pygame.quit()
sys.exit()
