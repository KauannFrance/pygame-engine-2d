import pygame

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
        self.speed = 10
        self.sound_disparo = pygame.mixer.Sound('tiro_espin.mp3')
        self.sound_disparo.set_volume(0.5)
        self.som_disparado = False

    def update(self):
        if self.direction == 'esquerda':
            self.rect.x -= self.speed
        elif self.direction == 'direita':
            self.rect.x += self.speed
        elif self.direction == 'cima':
            self.rect.y -= self.speed
        elif self.direction == 'baixo':
            self.rect.y += self.speed

        if not self.som_disparado:
            self.sound_disparo.play()
            self.som_disparado = True

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