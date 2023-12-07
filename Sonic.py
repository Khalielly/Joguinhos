import pygame
import sys
import random

pygame.init()

largura, altura = 800, 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("SONICÃO")

branco = (255, 255, 255)

heroi_direita = pygame.transform.scale(pygame.image.load("Game/Sonic/bd/heroi/direta.png"), (50, 50))
heroi_esquerda = pygame.transform.scale(pygame.image.load("Game/Sonic/bd/heroi/esquerda.png"), (50, 50))
inimigo_direita = pygame.transform.scale(pygame.image.load("Game/Sonic/bd/inimigo/01.png"), (50, 50))
inimigo_esquerda = pygame.transform.scale(pygame.image.load("Game/Sonic/bd/inimigo/02.png"), (50, 50))
moeda_imagem = pygame.transform.scale(pygame.image.load("Game/Sonic/bd/item/anel.png"), (50, 50))
fundo_imagem = pygame.transform.scale(pygame.image.load("Game/Sonic/bd/cenario/fundo.png"), (largura, altura))

pygame.mixer.music.load("Game/Sonic/bd/musica/tema4.mp3")
pygame.mixer.music.play(-1)

heroi_x, heroi_y = 50, altura - 150
heroi_velocidade, heroi_pulo, heroi_orientacao = 5, 20, "direita"

inimigo_x, inimigo_y = largura - 100, altura - 150
inimigo_velocidade, inimigo_orientacao = 5, "esquerda"

moedas, pontuacao = [(random.randint(50, largura - 50), altura - 150)], 0
esta_pulando, contagem_pulos = False, 10

def criar_nova_moeda():
    return random.randint(50, largura - 50), altura - 150

relogio = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] and heroi_x > 0:
        heroi_x -= heroi_velocidade
        heroi_orientacao = "esquerda"

    if teclas[pygame.K_RIGHT] and heroi_x < largura - 50:
        heroi_x += heroi_velocidade
        heroi_orientacao = "direita"

    if teclas[pygame.K_SPACE] and contagem_pulos > 0 and not esta_pulando:
        esta_pulando = True

    if esta_pulando:
        if heroi_y > altura - 250:
            heroi_y -= heroi_pulo
        else:
            esta_pulando = False

    elif heroi_y < altura - 150:
        heroi_y += heroi_pulo

    elif not esta_pulando:
        contagem_pulos = 10

    if inimigo_x <= 0 or inimigo_x >= largura - 50:
        inimigo_velocidade *= -1
        inimigo_orientacao = "esquerda" if inimigo_velocidade > 0 else "direita"
    inimigo_x += inimigo_velocidade

    for posicao_moeda in moedas:
        moeda_x, moeda_y = posicao_moeda
        if heroi_x < moeda_x + 40 < heroi_x + 50 and heroi_y < inimigo_y + 40 < heroi_y + 50:
            moedas.remove(posicao_moeda)
            moedas.append(criar_nova_moeda())
            pontuacao += 10

    if heroi_x < inimigo_x + 40 < heroi_x + 50 and heroi_y < inimigo_y + 40 < heroi_y + 50:
        fonte = pygame.font.Font(None, 72)
        texto_fim_de_jogo = fonte.render("Game Over", True, branco)
        janela.blit(texto_fim_de_jogo, (largura // 2 - 150, altura // 2 - 36))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    janela.blit(fundo_imagem, (0, 0))
    janela.blit(heroi_direita if heroi_orientacao == "direita" else heroi_esquerda, (heroi_x, heroi_y))
    janela.blit(inimigo_direita if inimigo_orientacao == "direita" else inimigo_esquerda, (inimigo_x, inimigo_y))

    for posicao_moeda in moedas:
        janela.blit(moeda_imagem, posicao_moeda)

    fonte = pygame.font.Font(None, 36)
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, branco)
    janela.blit(texto_pontuacao, (10, 10))

    pygame.display.flip()
    relogio.tick(30)
