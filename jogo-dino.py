import pygame
from pygame.locals import *
from sys import exit
from random import randrange, choice
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
sprite_sheet = pygame.image.load(os.path.join(diretorio_img, "Jogo-dino-Spritesheets2.png")).convert_alpha()

#som_colisao = pygame.mixer.Sound(os.path.join(diretorio_audio, 'nome_arquivo'))
#self.som_pular.set_volume(1) #aumentar o som da colisao
colidiu = False
escolha_obstaculo = choice([0, 1])

#criando a classe do Dino
class Dino(pygame.sprite.Sprite): # Dino será um tipo de sprite.
    
    def __init__(self): #O método __init__ é o construtor da classe
        pygame.sprite.Sprite.__init__(self) # inicializando a classe pygame.sprite.Sprite
        
        #self.som_pular = pygame.mixer.Sound(os.path.join(diretorio_audio, 'nome_arquivo'))
        #self.som_pular.set_volume(1) #aumentar o som do pulo
        
        self.imagens_dinossauro = [] #crio uma lista que recebe a spritesheets
        for i in range(3):
            img = sprite_sheet.subsurface((i*32,0), (32,32))  #recortar o 3 primeiros frames
            img = pygame.transform.scale(img, (32*3, 32*3)) #aumentar o tamanho da imagem
            self.imagens_dinossauro.append(img)
        
        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista] #estamos definindo self.image como a primeira imagem na lista de imagens do dinossauro.

        self.rect = self.image.get_rect() #pegar o retangulo ao redor do frame
        self.mask = pygame.mask.from_surface(self.image) #criando uma máscara da sprite do dinossauro
        self.posicao_y_ini = Altura - 64 - 96//2 #pegando o canto superior esquerdo do frame
        self.rect.center = (100, Altura-64) #posicionar o retangulo
        self.pulo = False
        
    def pular(self): #se eu apertar espaço ele muda a variável pulo para true
        self.pulo = True
        #self.som_pular.play() #tocar som
    
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
      

todas_as_sprites = pygame.sprite.Group() #criando um grupo de sprites*
dino = Dino() #instanciando a class Dino
todas_as_sprites.add(dino) #Criando uma instância da classe Dino e a adicionamos ao grupo de sprites.

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

for i in range(4): #criando 4 nuvens
    nuvem = Nuvens() #instanciando a class nuvens
    todas_as_sprites.add(nuvem)
    
#criando a classe do chão
class Chao(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = Altura - 32 * 2  # Altura do chão é 32*2 pixels

largura_chao = Largura // (32 * 2)  # Determina quantos sprites do chão são necessários para preencher a largura da tela
chao_sprites = pygame.sprite.Group()  # Cria um grupo para os sprites do chão
for i in range(largura_chao):  # Cria os sprites do chão e os posiciona
    chao = Chao(i * 32 * 2)  # Multiplica por 32*2 para garantir que os sprites se encaixem perfeitamente
    chao_sprites.add(chao)
    
# Adicionando os sprites do chão ao grupo de todas as sprites
todas_as_sprites.add(chao_sprites)

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect() #pegar o retangulo do cacto para posicionar ele na tela
        self.mask = pygame.mask.from_surface(self.image) #criando uma máscara da sprite do cactp
        self.escolha = escolha_obstaculo 
        self.rect.center = (Largura, Altura - 64*1.1)
        self.rect.x = Largura

    
    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = Largura #volta para o inicio
            self.rect.x -= 10 #vai se movimentar a cada 10 frames do jogo

        
cacto = Cacto()
todas_as_sprites.add(cacto)

class Maritaca(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_maritaca = []
        for i in range(8, 10):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))  # recorta os dois últimos frames
            img = pygame.transform.scale(img, (32 * 2, 32 * 2))  # aumenta o tamanho da imagem
            self.imagens_maritaca.append(img)
        
        self.index_lista = 0
        self.image = self.imagens_maritaca[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image) #criando uma máscara da sprite da maritaca para colisao
        self.escolha = escolha_obstaculo 
        self.rect = self.image.get_rect() #pegar o retangulo ao redor do frame
        self.rect.center = (Largura, 300) #posicionar o retangulo
        self.rect.x = Largura
    
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = Largura #volta para o inicio
            self.rect.x -= 10 #vai se movimentar a cada 10 frames do jogo
            if self.index_lista > 1: #criando o efeito de looping
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_maritaca[int(self.index_lista)]
            
maritaca = Maritaca()
todas_as_sprites.add(maritaca)

grupo_obstaculo = pygame.sprite.Group() #criando um grupo de obstáculos
grupo_obstaculo.add(cacto) #add os obstáculos dentro do grupo
grupo_obstaculo.add(maritaca) #add os obstáculos dentro do grupo

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
    
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculo, False, pygame.sprite.collide_mask) #lista de colisões, vai receber o objeto que colidiu com o dino
    todas_as_sprites.draw(tela) # Desenha todos os sprites do grupo 
    
    if cacto.rect.topright[0] <= 0 or maritaca.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        cacto.rect.x = Largura
        maritaca.rect.x = Largura
        cacto.escolha = escolha_obstaculo
        maritaca.escolha = escolha_obstaculo
            
    if colisoes and colidiu == False:
        #som_colisao.play()
        colidiu = True
        #pass #tirar quando inserir o som
    if colidiu == True:
       pass
    else:
        todas_as_sprites.update() # Atualiza todos os sprites no grupo 
 
    pygame.display.flip() # Atualiza a tela inteira para o usuário ver as mudanças.
        