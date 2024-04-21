import pygame
from pygame.locals import *
from sys import exit
from random import randrange
import os

pygame.init()
pygame.mixer.init()

diretorio_princ = os.path.dirname(__file__) #caminho do jogo
diretorio_img = os.path.join(diretorio_princ, 'Imagens')
#diretorio_audio =  os.path.join(diretorio_princ, 'Audios')

Largura = 640 #da tela
Altura = 480 #da tela

BRANCO = (255, 255, 255)

tela = pygame.display.set_mode((Largura, Altura))

pygame.display.set_caption('Dino Game') #definimos o título da janela do jogo como 'Dino'.
sprite_sheet = pygame.image.load(os.path.join(diretorio_img, "Jogo-dino-Spritesheets.png")).convert_alpha()

#criando a classe do Dino
class Dino(pygame.sprite.Sprite): # Dino será um tipo de sprite.
    def __init__(self): #O método __init__ é o construtor da classe
        pygame.sprite.Sprite.__init__(self) # inicializando a classe pygame.sprite.Sprite
        
        #self.som_pular = pygame.mixer.Sound(os.path.join(diretorio_audio, 'nome_arquivo'))
        self.som_pular.set_volume(1) #aumentar o som do pulo
        
        self.imagens_dinossauro = [] #crio uma lista que recebe a spritesheets
        for i in range(3):
            img = sprite_sheet.subsurface((i*32,0), (32,32))  #recortar o 3 primeiros frames
            img = pygame.transform.scale(img, (32*3, 32*3)) #aumentar o tamanho da imagem
            self.imagens_dinossauro.append(img)
        
        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista] #estamos definindo self.image como a primeira imagem na lista de imagens do dinossauro.

        self.rect = self.image.get_rect() #pegar o retangulo ao redor do frame
        self.posicao_y_ini = Altura - 64 - 96//2 #pegando o canto superior esquerdo do frame
        self.rect.center = (100, Altura-64) #posicionar o retangulo
        self.pulo = False
        
    def pular(self): #se eu apertar espaço ele muda a variável pulo para true
        self.pulo = True
        self.som_pular.play() #tocar som
    
    #metodo update 
    def update(self): #estamos atualizando a imagem do dinossauro para criar uma animação. 
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False  
            self.rect.y -= 20 #muda a posicao do y para pular
        else:
            if self.rect.y < self.posicao_y_ini:
                self.rect.y += 20
            else:
                self.rect.y = self.posicao_y_ini
        if self.index_lista > 2: #criando o efeito de looping
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]
      
        
#criando a classe das nuvens
class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32,0), (32,32))
        self.image = pygame.transform.scale( self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.x = Largura - randrange(30, 300, 90) #varia a posicao da nuvem em x
        
    def update(self):
        if self.rect.topright[0] < 0:
           self.rect.x = Largura #volta para o inicio
           self.rect.y = randrange(50, 200, 50) #intervalo de 50 e 200 variando de 50 em 50
        self.rect.x -= 10 #vai se movimentar a cada 10 frames do jogo
    
todas_as_sprites = pygame.sprite.Group() #criando um grupo de sprites*
dino = Dino() #instanciando a class Dino
todas_as_sprites.add(dino) #Criando uma instância da classe Dino e a adicionamos ao grupo de sprites.
for i in range(4): #criando 4 nuvens
    nuvem = Nuvens() #instanciando a class nuvens
    todas_as_sprites.add(nuvem)

relogio = pygame.time.Clock() #Criamos um objeto de relógio
while True:
    relogio.tick(30) #Limita o jogo a rodar a 30 frames por segundo.
    tela.fill(BRANCO) # Preenche a tela com a cor branca a cada iteração do loop
    for event in pygame.event.get():
        if event.type == QUIT: #Se o evento for do tipo QUIT (fechar a janela), o jogo é encerrado.
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE: #se a tecla for igual à espaco, então chama a função pular
                if dino.rect.y != dino.posicao_y_ini: #impede de apertar espaço várias vezes
                    pass
                else:
                    dino.pular()
    todas_as_sprites.draw(tela) # Desenha todos os sprites do grupo 
    todas_as_sprites.update() # Atualiza todos os sprites no grupo 
    
    pygame.display.flip() # Atualiza a tela inteira para o usuário ver as mudanças.
        