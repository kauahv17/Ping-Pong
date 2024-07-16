import pygame
from random import randint,uniform

tamanho_tela = (900,600)

tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Ping Pong")

COR = {
        "branco": (255,255,255),
        "preto":(0,0,0),
        "azul":(0,0,255),
        "vermelho":(255,0,0),
        "verde": (0,255,0),
    }

class JOGO:
    tamanho_tela = (900,600)
    COR = {
        "verde escuro": (0,150,0),
        "cinza": (100,100,100)
    }
    
    def __init__(self, modo = None):
        self.altura = 400
        self.largura = 600
        self.acabou = False
        self.reiniciar = False
        self.iniciou = False
        self.modo = modo
        pygame.font.init()
        self.fonte=pygame.font.get_default_font()
        self.fontesys=pygame.font.SysFont(self.fonte, 40)

    def construir_popup(self, largura, altura):
        x = (tamanho_tela[0] / 2) - (largura / 2)
        y = (tamanho_tela[1] / 2) - (altura / 2)

        return pygame.Rect(x, y, largura, altura)
    
    def atualizar_placar(self, tela, pontuacao_jg1, pontuacao_jg2):
        txt = f'{pontuacao_jg1}  X  {pontuacao_jg2}'
        txt_tela = self.fontesys.render(txt, 1, COR["branco"])
        tela.blit(txt_tela,((tamanho_tela[0] / 2) - 40,30))

    def desenhar(self, tela):
        borda = self.construir_popup(self.largura + 5, self.altura + 5)
        popup = self.construir_popup(self.largura, self.altura)
        pygame.draw.rect(tela, self.COR["verde escuro"], borda)# borda info
        pygame.draw.rect(tela, self.COR["cinza"], popup)# tela info

        txt0='ESCOLHA O MODO DE JOGO'
        txt1='Multiplayer("M")'
        txt2='Bot("B")'
        textos = [txt1, txt2]
        
        fontesys=pygame.font.SysFont(self.fonte, 60)

        txt_tela = fontesys.render(txt0, 1, (0,0,0))
        text_X = (tamanho_tela[0] / 2) - (self.largura / 2 - 8)
        text_Y = (tamanho_tela[1] / 2) - 100
        tela.blit(txt_tela,(text_X,text_Y))

        for i,txt in enumerate(textos):
            txt_tela = fontesys.render(txt, 1, (0,0,0))
            text_X = (tamanho_tela[0] / 2) - (self.largura / 2 - 50)
            text_Y = (tamanho_tela[1] / 2) - 50
            tela.blit(txt_tela,(text_X,text_Y+ 70*(i+1)))

# jogadores
class JOGADOR:
    pygame.font.init()
    fonte=pygame.font.get_default_font()
    fontesys=pygame.font.SysFont(fonte, 40)

    tamanho_tela = (900,600)
    COR = {
        "branco": (255,255,255),
        "vermelho escuro":(100,0,0),
        "verde": (0,255,0),
        "verde escuro": (0,100,0),
    }
    def __init__(self):
        self.intensidade = 80
        self.altura = 80
        self.largura = 20
        self.altura_inicial = (tamanho_tela[1] / 2) - (self.altura / 2)
        self.cima = -1 * (self.intensidade / 100)
        self.baixo = 1 * (self.intensidade / 100)
        self.neutra = 0

    def mensagem_tela(self, tela):
        txt1 = 'Reiniciar("R")'
        txt_tela = self.fontesys.render(txt1, 1, COR["branco"])
        tela.blit(txt_tela,((tamanho_tela[0] / 2) -85,220))

        txt2 = 'Trocar de Modo("T")'
        txt_tela = self.fontesys.render(txt2, 1, COR["branco"])
        tela.blit(txt_tela,((tamanho_tela[0] / 2) -120,300))

# jogador 1 (ESQUERDA)
class JGDR_1(JOGADOR):
    def __init__(self, posY = None, cor = COR["azul"], pontos = 0):
        super().__init__()
        self.X = 30
        if posY == None:
            self.Y = self.altura_inicial
        else:
            self.Y = posY
        self.Cor = cor
        self.pontos = pontos
        self.direcao = self.neutra
        self.bloco = self.contruir_bloco()
        self.golX = 0
        self.marcou = False

    def contruir_bloco(self):
        return pygame.Rect(self.X, self.Y, self.largura, self.altura)
    
    def mudar_direcao(self, nova_direcao):
        if (nova_direcao, self.direcao) == (self.cima, self.baixo) or (nova_direcao, self.direcao) == (self.baixo, self.cima):
            self.direcao = 0
        else:
            self.direcao = nova_direcao

    def mover(self):
        if self.Y < 0:
            self.Y = self.neutra
            self.direcao = self.neutra
            return
        
        if (self.Y + self.altura) > self.tamanho_tela[1]:
            self.Y = self.tamanho_tela[1] - self.altura
            self.direcao = self.neutra
            return
        
        self.Y += self.direcao

    def contruir_gol(self, tela, cor = COR["verde"]):
        gol = pygame.Rect(0, 0, 5, tamanho_tela[1])
        pygame.draw.rect(tela, cor, gol)# gol do jogador 1

    def verificar_placar(self, tela, bolaX):
        if bolaX <= 0:
            if not self.marcou:
                self.pontos += 1
            self.mensagem_tela(tela)
            self.contruir_gol(tela, self.COR["vermelho escuro"])
            self.marcou = True

    def desenhar(self, tela):
        self.bloco = self.contruir_bloco()
        pygame.draw.rect(tela, self.Cor, self.bloco)# jogador 1
        self.contruir_gol(tela)

    def reiniciar(self):
        self.__init__(pontos = self.pontos)

# jogador 2 (DIREITA)
class JGDR_2(JOGADOR):
    def __init__(self, posY = None, cor = COR["vermelho"], bot = False, pontos = 0):
        super().__init__()
        self.X = self.tamanho_tela[0] - 50
        if posY == None:
            self.Y = self.altura_inicial
        else:
            self.Y = posY
        self.bot = bot
        self.Cor = cor
        self.pontos = pontos
        self.direcao = self.neutra
        self.bloco = self.contruir_bloco()
        self.tocou = False
        self.golX = tamanho_tela[0]-5
        self.campoX = tamanho_tela[0] - (tamanho_tela[0]/3.5)
        self.vantagem = self.calcular_vantagem()
        self.marcou = False

    def contruir_bloco(self):
        return pygame.Rect(self.X, self.Y, self.largura, self.altura)
    
    def calcular_vantagem(self):
        N = uniform(1,1.6)
        return N
    
    def mudar_direcao(self, nova_direcao):
        if not self.bot:
            if (nova_direcao, self.direcao) == (self.cima, self.baixo) or (nova_direcao, self.direcao) == (self.baixo, self.cima):
                self.direcao = 0
            else:
                self.direcao = nova_direcao
        else:
            bolaX,bolaY = nova_direcao

            #print(self.tocou)
            if bolaX > self.campoX and not self.tocou:
                
                #print(bolaY, self.Y)
                if bolaY < (self.Y + (self.altura/3 * 2)):
                    self.direcao = self.cima * self.vantagem

                elif bolaY > (self.Y + (self.altura/3 * 2)):
                    self.direcao = self.baixo * self.vantagem
                
            else:
                self.direcao = self.neutra
                self.tocou = False

    def mover(self):
        if self.Y < 0:
            self.Y = self.neutra
            self.direcao = self.neutra
            return
        
        if (self.Y + self.altura) > self.tamanho_tela[1]:
            self.Y = self.tamanho_tela[1] - self.altura
            self.direcao = self.neutra
            return
        
        self.Y += self.direcao

    def contruir_gol(self, tela, cor = COR["verde"]):
        gol = pygame.Rect(self.golX, 0, 5, tamanho_tela[1])
        pygame.draw.rect(tela, cor, gol)# gol do jogador 2
        if self.bot:
            campo = pygame.Rect(self.campoX, 0, 5, tamanho_tela[1])
            pygame.draw.rect(tela, self.COR["verde escuro"], campo)# campo do jogador 2 (BOT)

    def verificar_placar(self, tela, bolaX):
        if bolaX >= self.golX:
            if not self.marcou:
                self.pontos += 1
            self.mensagem_tela(tela)
            self.contruir_gol(tela, self.COR["vermelho escuro"])
            self.marcou = True

    def desenhar(self, tela):
        self.bloco = self.contruir_bloco()
        pygame.draw.rect(tela, self.Cor, self.bloco)# jogador 2
        self.contruir_gol(tela)

    def reiniciar(self):
        self.__init__(bot = True, pontos = self.pontos)

class BOLA(JOGADOR):
    def __init__(self, lance_inicial):
        super().__init__()
        self.rebatidas = 0
        self.intensidade_bola = 90#%
        self.tamanho = 15

        self.X = (tamanho_tela[0] / 2) - (self.tamanho / 2)
        self.Y = (tamanho_tela[1] / 2) - (self.tamanho / 2)

        self.direcaoX = lance_inicial[0]
        self.direcaoY = lance_inicial[1]

        self.velocidadeX = self.atualizar_velocidade(self.direcaoX)
        self.velocidadeY = self.atualizar_velocidade(self.direcaoY)
        
        self.tocou1 = False
        self.tocou2 = False

        self.Cor = COR["branco"]
        self.bola = self.construir_bola()

    def comecou(self, situacao):
        if situacao != False:
            return True
        return False

    def atualizar_velocidade(self, eixo):
        return eixo * ((self.intensidade_bola + (5 * (self.rebatidas // 3))) / 100)
    
    def verificar_colisao(self, jgdr1, jgdr2):
    
        if jgdr1.collidepoint(self.X, self.Y) or jgdr2.collidepoint(self.X, self.Y):
            
            if jgdr1.collidepoint(self.X, self.Y) and not self.tocou1:
                self.tocou1 = True
                self.tocou2 = False
                self.rebatidas += 1
            if jgdr2.collidepoint(self.X, self.Y) and not self.tocou2:
                self.tocou2 = True
                self.tocou1 = False
                self.rebatidas += 1
            

            self.direcaoX = -self.direcaoX
            
            self.velocidadeX = self.atualizar_velocidade(eixo=self.direcaoX)
            self.velocidadeY = self.atualizar_velocidade(eixo=self.direcaoY)

        return jgdr2.collidepoint(self.X, self.Y)

    def colisao_parede(self):
        if self.Y < 0 or (self.Y + self.tamanho) > tamanho_tela[1]:
            self.direcaoY = -self.direcaoY
            self.velocidadeY = self.atualizar_velocidade(self.direcaoY)

    def mover(self, situacao):
        if self.comecou(situacao):
            self.X += self.velocidadeX
            self.Y += self.velocidadeY

    def construir_bola(self):
        return pygame.Rect(self.X, self.Y, self.tamanho, self.tamanho)

    def desenhar(self, tela):
        self.bola = self.construir_bola()
        pygame.draw.rect(tela, self.Cor, self.bola)# bola

def escolher_direcao():
    while True:
        N = randint(-1,1)
        if N != 0:
            return N

def jogar(modo = None, jg1=0, jg2=0):
    jogo = JOGO(modo)
    
    jogador1 = JGDR_1(pontos=jg1)
    jogador2 = JGDR_2(pontos=jg2)
    if jogo.modo == "BOT":
        jogador2 = JGDR_2(bot=True,pontos=jg2)

    lanceX = escolher_direcao()
    lanceY = escolher_direcao()

    bola = BOLA([lanceX, lanceY])
    #print([lanceX, lanceY])
    #print(jogador2.vantagem)

    direcao = JOGADOR()

    while not jogo.acabou:
        tela.fill(COR["preto"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogo.acabou = True

            if event.type == pygame.KEYDOWN:
                if jogo.modo == None:
                    if event.key == pygame.K_m:
                        jogo.modo = "multiplayer"
                        
                    if event.key == pygame.K_b:
                        jogo.modo = "BOT"
                        jogador2.bot = True

                else:
                    if event.key == pygame.K_t:
                        jogo.modo = None
                        event.key = pygame.K_r

                    if event.key == pygame.K_w:
                        jogador1.mudar_direcao(direcao.cima)
                        jogo.iniciou = True
                    if event.key == pygame.K_s:
                        jogador1.mudar_direcao(direcao.baixo)
                        jogo.iniciou = True

                    if jogador2.bot == False and jogo.acabou == False:
                        if event.key == pygame.K_UP:
                            jogador2.mudar_direcao(direcao.cima)
                            jogo.iniciou = True
                        if event.key == pygame.K_DOWN:
                            jogador2.mudar_direcao(direcao.baixo)
                            jogo.iniciou = True

                    if event.key == pygame.K_r:
                        jogo.acabou = True
                        jogo.reiniciar = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    jogador1.mudar_direcao(direcao.neutra)

                if jogador2.bot == False and jogo.acabou == False:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        jogador2.mudar_direcao(direcao.neutra)

        jogador2.tocou = bola.verificar_colisao(jogador1.bloco, jogador2.bloco)
        if jogador2.bot:
            jogador2.mudar_direcao((bola.X, bola.Y))

        bola.colisao_parede()

        bola.desenhar(tela)# bola
        
        bola.mover(jogo.iniciou)

        jogador1.desenhar(tela)# jogador 1
        jogador2.desenhar(tela)# jogador 2 

        jogador1.mover()
        jogador2.mover()

        if jogo.modo == None:
            jogo.desenhar(tela)

        jogador1.verificar_placar(tela,bola.X)
        jogador2.verificar_placar(tela,bola.X)
        jogo.atualizar_placar(tela, jogador2.pontos, jogador1.pontos)

        pygame.time.wait(1)
        pygame.display.flip()

    if jogo.modo == None:
            jogar(jogo.modo, 0, 0)

    if jogo.reiniciar:
        jogar(jogo.modo, jogador1.pontos, jogador2.pontos)

    pygame.quit()

if __name__ == "__main__":
    jogar()
