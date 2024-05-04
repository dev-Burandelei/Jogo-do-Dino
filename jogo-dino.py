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

#som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_audio, 'nome_arquivo'))
#self.som_pontuacao.set_volume(1) #aumentar o som da pontuacao

#som_colisao = pygame.mixer.Sound(os.path.join(diretorio_audio, 'nome_arquivo'))
#self.som_pular.set_volume(1) #aumentar o som da colisao
colidiu = False
escolha_obstaculo = choice([0, 1])
pontos_do_jogo = 0
velocidade_do_jogo = 10

def pontuacao(mensagem, tam_font, cor_texto):
    fonte = pygame.font.SysFont('comicsansms', tam_font, True, False) #fonte do texto
    msg = f'{mensagem}'
    texto_final = fonte.render(msg, True, cor_texto)
    return texto_final

def mensagem_botao(mensagem, tam_font, cor_texto, cor_botao):
    fonte = pygame.font.SysFont('arial', tam_font, True, False) #fonte do texto
    texto = fonte.render(mensagem, True, cor_texto)
    texto_rect = texto.get_rect(center=(Largura/2, Altura - 90))

    # Criar um retângulo para representar o botão
    largura_botao = texto_rect.width + 20  # Adicione um espaço extra em ambos os lados do texto
    altura_botao = texto_rect.height + 20  # Adicione um espaço extra em cima e embaixo do texto
    botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
    botao_rect.center = texto_rect.center  # Centraliza o retângulo no texto

    # Desenhar o retângulo do botão na tela
    pygame.draw.rect(tela, cor_botao, botao_rect)

    # Desenhar o texto na tela
    tela.blit(texto, texto_rect)

def tela_start():
    dino_fundo = os.path.join(diretorio_img, "dino-capa.png")        
    dino_fundo = pygame.image.load(dino_fundo).convert()
    # Redimensiona a imagem de fundo para o tamanho da tela
    dino_fundo = pygame.transform.scale(dino_fundo, (Largura, Altura))
     # Desenha a imagem de fundo na superfície da tela
    tela.blit(dino_fundo, (0, 0))

    mensagem_botao('Pressione uma tecla para jogar', 20, (0,0,0), (200, 200, 200))
    #texto = mensagem('Pressione uma tecla para jogar', 40, (0,0,0))
    # Define a posição do texto
    #texto_rect = texto.get_rect(center=(Largura/2, Altura/2))
    # Desenha o texto na tela
    #tela.blit(texto, texto_rect)
    pygame.display.flip()
    esperar_jogador()
    
def esperar_jogador():
    esperando = True
    while esperando:
        relogio.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
            if event.type == pygame.KEYUP:
                esperando = False
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
        self.rect.x -= velocidade_do_jogo #vai se movimentar a cada 10 frames do jogo

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
        self.velocidade = 10  # Velocidade de movimento do chão

    def update(self):
        self.rect.x -= self.velocidade  # Move o chão para a esquerda
        if self.rect.right < 0:  # Se o sprite do chão sair da tela à esquerda
            self.rect.x += Largura  # Move o sprite do chão para o final da tela

# Criação dos sprites do chão
largura_chao = Largura // (32 * 2) + 2  # Determina quantos sprites do chão são necessários para preencher a largura da tela
chao_sprites = pygame.sprite.Group()  # Cria um grupo para os sprites do chão
for i in range(largura_chao):  # Cria os sprites do chão e os posiciona
    chao = Chao(i * 32 * 2)  # Multiplica por 32*3 para garantir que os sprites se encaixem perfeitamente
    chao_sprites.add(chao)

# Adicionando o grupo de sprites do chão ao grupo de todas as sprites
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
            self.rect.x -= velocidade_do_jogo #vai se movimentar a cada 10 frames do jogo

        
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
            self.rect.x -= velocidade_do_jogo #vai se movimentar a cada 10 frames do jogo
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

tela_start()

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
        if pontos_do_jogo % 100 == 0:
            pontos_do_jogo += 1
        pass
    else:
        pontos_do_jogo += 1 # a cada interação do jogo no loop orincipal soma 1 ponto
        todas_as_sprites.update() # Atualiza todos os sprites no grupo 
        exibir_pontuacao = pontuacao(pontos_do_jogo, 40, (0,0,0))
        
    if pontos_do_jogo % 100 ==  0:
        #som_pontuacao.play()
        if velocidade_do_jogo >= 23:
            velocidade_do_jogo += 0 #velocidade continua constante
        else:
            velocidade_do_jogo += 1
        
        #print(velocidade_do_jogo)
            
    tela.blit(exibir_pontuacao, (520,30))
 
    pygame.display.flip() # Atualiza a tela inteira para o usuário ver as mudanças.
        